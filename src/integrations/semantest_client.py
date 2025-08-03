"""Semantest integration client for real-time prompt processing."""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass
import websockets
from websockets.exceptions import WebSocketException


@dataclass
class SemantestConfig:
    """Configuration for Semantest connection."""
    websocket_url: str = "ws://localhost:8080/ws"
    api_key: Optional[str] = None
    reconnect_interval: int = 5
    max_reconnect_attempts: int = 10


class SemantestClient:
    """Client for integrating with Semantest image generation service."""
    
    def __init__(self, config: Optional[SemantestConfig] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or SemantestConfig()
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.is_connected = False
        self.reconnect_attempts = 0
        self.message_handlers: Dict[str, Callable] = {}
        self._running = False
        
    async def connect(self) -> bool:
        """Connect to Semantest WebSocket server."""
        try:
            self.logger.info(f"Connecting to Semantest at {self.config.websocket_url}")
            
            # Add authentication headers if API key provided
            headers = {}
            if self.config.api_key:
                headers["Authorization"] = f"Bearer {self.config.api_key}"
            
            self.websocket = await websockets.connect(
                self.config.websocket_url,
                extra_headers=headers
            )
            
            self.is_connected = True
            self.reconnect_attempts = 0
            self.logger.info("Successfully connected to Semantest")
            
            # Send initial handshake
            await self._handshake()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to Semantest: {str(e)}")
            self.is_connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from Semantest."""
        self._running = False
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            self.is_connected = False
            self.logger.info("Disconnected from Semantest")
    
    async def send_prompt(self, prompt_data: Dict[str, Any]) -> str:
        """Send a prompt to Semantest for image generation."""
        if not self.is_connected:
            raise ConnectionError("Not connected to Semantest")
        
        # Generate request ID
        import uuid
        request_id = str(uuid.uuid4())
        
        # Prepare message
        message = {
            "type": "generate_image",
            "request_id": request_id,
            "data": {
                "prompt": prompt_data.get("prompt", ""),
                "negative_prompt": prompt_data.get("negative_prompt", ""),
                "parameters": {
                    "width": prompt_data.get("width", 1024),
                    "height": prompt_data.get("height", 1024),
                    "steps": prompt_data.get("steps", 30),
                    "guidance_scale": prompt_data.get("guidance_scale", 7.5),
                    "seed": prompt_data.get("seed", -1),
                    "style": prompt_data.get("style", "comic book")
                },
                "metadata": prompt_data.get("metadata", {})
            }
        }
        
        # Send message
        await self.websocket.send(json.dumps(message))
        self.logger.debug(f"Sent prompt request: {request_id}")
        
        return request_id
    
    async def send_batch(self, prompts: list[Dict[str, Any]]) -> str:
        """Send a batch of prompts for processing."""
        if not self.is_connected:
            raise ConnectionError("Not connected to Semantest")
        
        # Generate batch ID
        import uuid
        batch_id = str(uuid.uuid4())
        
        # Prepare batch message
        message = {
            "type": "batch_generate",
            "batch_id": batch_id,
            "data": {
                "prompts": prompts,
                "priority": "normal",
                "callback_url": None  # Optional webhook for completion
            }
        }
        
        # Send message
        await self.websocket.send(json.dumps(message))
        self.logger.info(f"Sent batch of {len(prompts)} prompts: {batch_id}")
        
        return batch_id
    
    def on_message(self, message_type: str, handler: Callable):
        """Register a message handler for specific message types."""
        self.message_handlers[message_type] = handler
        self.logger.debug(f"Registered handler for message type: {message_type}")
    
    async def listen(self):
        """Listen for messages from Semantest."""
        self._running = True
        
        while self._running:
            try:
                if not self.is_connected:
                    # Try to reconnect
                    if self.reconnect_attempts < self.config.max_reconnect_attempts:
                        self.logger.info(f"Attempting to reconnect... ({self.reconnect_attempts + 1}/{self.config.max_reconnect_attempts})")
                        if await self.connect():
                            self.reconnect_attempts = 0
                        else:
                            self.reconnect_attempts += 1
                            await asyncio.sleep(self.config.reconnect_interval)
                    else:
                        self.logger.error("Max reconnection attempts reached. Stopping listener.")
                        break
                    continue
                
                # Receive message
                message = await self.websocket.recv()
                data = json.loads(message)
                
                # Handle message
                await self._handle_message(data)
                
            except WebSocketException as e:
                self.logger.error(f"WebSocket error: {str(e)}")
                self.is_connected = False
            except json.JSONDecodeError as e:
                self.logger.error(f"Failed to parse message: {str(e)}")
            except Exception as e:
                self.logger.error(f"Unexpected error in listener: {str(e)}")
                await asyncio.sleep(1)
    
    async def _handshake(self):
        """Perform initial handshake with Semantest."""
        handshake = {
            "type": "handshake",
            "client": "metaphysical-scene-weaver",
            "version": "0.1.0",
            "capabilities": ["batch_processing", "real_time", "metadata_tracking"]
        }
        
        await self.websocket.send(json.dumps(handshake))
        
        # Wait for acknowledgment
        response = await self.websocket.recv()
        data = json.loads(response)
        
        if data.get("type") == "handshake_ack":
            self.logger.info("Handshake successful")
        else:
            self.logger.warning("Unexpected handshake response")
    
    async def _handle_message(self, data: Dict[str, Any]):
        """Handle incoming message from Semantest."""
        message_type = data.get("type")
        
        if message_type in self.message_handlers:
            try:
                await self.message_handlers[message_type](data)
            except Exception as e:
                self.logger.error(f"Error in message handler for {message_type}: {str(e)}")
        else:
            self.logger.debug(f"Unhandled message type: {message_type}")
    
    async def get_status(self, request_id: str) -> Dict[str, Any]:
        """Get status of a specific generation request."""
        if not self.is_connected:
            raise ConnectionError("Not connected to Semantest")
        
        message = {
            "type": "get_status",
            "request_id": request_id
        }
        
        await self.websocket.send(json.dumps(message))
        
        # In a real implementation, you'd wait for the response
        # This is simplified for demonstration
        return {"status": "pending"}
    
    async def cancel_request(self, request_id: str) -> bool:
        """Cancel a generation request."""
        if not self.is_connected:
            raise ConnectionError("Not connected to Semantest")
        
        message = {
            "type": "cancel_request",
            "request_id": request_id
        }
        
        await self.websocket.send(json.dumps(message))
        return True


class SemantestIntegration:
    """High-level integration class for Scene Weaver."""
    
    def __init__(self, scene_weaver: 'SceneWeaver', config: Optional[SemantestConfig] = None):
        self.scene_weaver = scene_weaver
        self.client = SemantestClient(config)
        self.logger = logging.getLogger(__name__)
        self.pending_requests: Dict[str, Dict[str, Any]] = {}
        
    async def start(self):
        """Start the integration."""
        # Connect to Semantest
        if await self.client.connect():
            # Register message handlers
            self.client.on_message("image_ready", self._handle_image_ready)
            self.client.on_message("generation_error", self._handle_generation_error)
            self.client.on_message("progress_update", self._handle_progress_update)
            
            # Start listening
            asyncio.create_task(self.client.listen())
            
            self.logger.info("Semantest integration started")
            return True
        
        return False
    
    async def process_and_generate(self, script_entry: 'ScriptEntry', context: list = None) -> str:
        """Process a script entry and send to Semantest for generation."""
        # Process with Scene Weaver
        index = 0
        all_entries = context or [script_entry]
        enriched_scene = self.scene_weaver.process_entry(script_entry, index, all_entries)
        
        # Prepare prompt data
        prompt_data = {
            "prompt": enriched_scene.prompt,
            "negative_prompt": self.scene_weaver.prompt_generator.generate_negative_prompt(
                {"scene_complexity": enriched_scene.metadata.get("visual_complexity", "moderate")}
            ),
            "metadata": {
                "entry_id": enriched_scene.entry_id,
                "speaker": enriched_scene.metadata.get("speaker"),
                "philosophy": enriched_scene.philosophy.get("primary_concept"),
                "emotion": enriched_scene.emotion.get("primary"),
                "panel_count": enriched_scene.metadata.get("panel_count", 1)
            },
            "style": self.scene_weaver.prompt_generator.style.value
        }
        
        # Send to Semantest
        request_id = await self.client.send_prompt(prompt_data)
        
        # Track request
        self.pending_requests[request_id] = {
            "entry_id": enriched_scene.entry_id,
            "scene_data": enriched_scene,
            "status": "pending"
        }
        
        return request_id
    
    async def process_script_batch(self, script_path: Path) -> str:
        """Process entire script and send as batch to Semantest."""
        # Process script
        scenes = self.scene_weaver.process_script(script_path)
        
        # Prepare batch
        prompts = []
        for scene in scenes:
            prompt_data = {
                "entry_id": scene.entry_id,
                "prompt": scene.prompt,
                "negative_prompt": self.scene_weaver.prompt_generator.generate_negative_prompt(
                    {"scene_complexity": scene.metadata.get("visual_complexity", "moderate")}
                ),
                "metadata": scene.metadata,
                "parameters": {
                    "style": self.scene_weaver.prompt_generator.style.value
                }
            }
            prompts.append(prompt_data)
        
        # Send batch
        batch_id = await self.client.send_batch(prompts)
        
        self.logger.info(f"Sent batch {batch_id} with {len(prompts)} scenes")
        return batch_id
    
    async def _handle_image_ready(self, data: Dict[str, Any]):
        """Handle image ready notification."""
        request_id = data.get("request_id")
        image_url = data.get("image_url")
        
        if request_id in self.pending_requests:
            request_data = self.pending_requests[request_id]
            request_data["status"] = "completed"
            request_data["image_url"] = image_url
            
            self.logger.info(f"Image ready for entry {request_data['entry_id']}: {image_url}")
            
            # You could emit an event or call a callback here
    
    async def _handle_generation_error(self, data: Dict[str, Any]):
        """Handle generation error."""
        request_id = data.get("request_id")
        error = data.get("error")
        
        if request_id in self.pending_requests:
            request_data = self.pending_requests[request_id]
            request_data["status"] = "error"
            request_data["error"] = error
            
            self.logger.error(f"Generation error for entry {request_data['entry_id']}: {error}")
    
    async def _handle_progress_update(self, data: Dict[str, Any]):
        """Handle progress update."""
        request_id = data.get("request_id")
        progress = data.get("progress", 0)
        
        if request_id in self.pending_requests:
            request_data = self.pending_requests[request_id]
            request_data["progress"] = progress
            
            self.logger.debug(f"Progress update for {request_id}: {progress}%")