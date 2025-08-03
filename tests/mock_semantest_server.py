"""Mock Semantest WebSocket server for testing."""

import asyncio
import json
import logging
import websockets
from datetime import datetime
import random
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MockSemantestServer:
    """Mock Semantest server that simulates image generation."""
    
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.clients = set()
        self.active_requests = {}
        self.completed_requests = {}
        
    async def handle_client(self, websocket, path):
        """Handle a client connection."""
        client_id = str(uuid.uuid4())
        self.clients.add(websocket)
        logger.info(f"Client {client_id} connected from {websocket.remote_address}")
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(websocket, data)
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "error": "Invalid JSON"
                    }))
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "error": str(e)
                    }))
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
        finally:
            self.clients.remove(websocket)
    
    async def handle_message(self, websocket, data):
        """Handle different message types."""
        msg_type = data.get("type")
        logger.debug(f"Received message type: {msg_type}")
        
        if msg_type == "handshake":
            await self.handle_handshake(websocket, data)
            
        elif msg_type == "generate_image":
            await self.handle_generate_image(websocket, data)
            
        elif msg_type == "batch_generate":
            await self.handle_batch_generate(websocket, data)
            
        elif msg_type == "get_status":
            await self.handle_get_status(websocket, data)
            
        elif msg_type == "cancel_request":
            await self.handle_cancel_request(websocket, data)
            
        else:
            await websocket.send(json.dumps({
                "type": "error",
                "error": f"Unknown message type: {msg_type}"
            }))
    
    async def handle_handshake(self, websocket, data):
        """Handle handshake message."""
        logger.info(f"Handshake from {data.get('client')} v{data.get('version')}")
        
        response = {
            "type": "handshake_ack",
            "server": "mock_semantest",
            "version": "0.1.0",
            "capabilities": ["batch_processing", "real_time", "metadata_tracking"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await websocket.send(json.dumps(response))
    
    async def handle_generate_image(self, websocket, data):
        """Handle image generation request."""
        request_id = data.get("request_id")
        prompt_data = data.get("data", {})
        
        logger.info(f"Image generation request {request_id}: {prompt_data.get('prompt', '')[:50]}...")
        
        # Store request
        self.active_requests[request_id] = {
            "websocket": websocket,
            "prompt_data": prompt_data,
            "start_time": datetime.utcnow(),
            "status": "processing"
        }
        
        # Simulate generation process
        asyncio.create_task(self.simulate_generation(request_id, websocket))
    
    async def simulate_generation(self, request_id, websocket):
        """Simulate the image generation process."""
        try:
            # Send progress updates
            for progress in [10, 25, 50, 75, 90, 95, 100]:
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
                if request_id not in self.active_requests:
                    # Request was cancelled
                    return
                
                await websocket.send(json.dumps({
                    "type": "progress_update",
                    "request_id": request_id,
                    "progress": progress,
                    "stage": self.get_stage_name(progress)
                }))
            
            # Simulate final processing
            await asyncio.sleep(random.uniform(0.5, 1.0))
            
            # Send completion
            image_url = f"http://mock.semantest.com/images/{request_id}.png"
            
            await websocket.send(json.dumps({
                "type": "image_ready",
                "request_id": request_id,
                "image_url": image_url,
                "metadata": {
                    "generation_time": random.uniform(5, 15),
                    "model": "mock-diffusion-v1",
                    "size": [1024, 1024]
                }
            }))
            
            # Move to completed
            if request_id in self.active_requests:
                self.completed_requests[request_id] = {
                    **self.active_requests[request_id],
                    "status": "completed",
                    "image_url": image_url,
                    "end_time": datetime.utcnow()
                }
                del self.active_requests[request_id]
                
        except Exception as e:
            logger.error(f"Error in generation simulation: {e}")
            
            # Send error
            try:
                await websocket.send(json.dumps({
                    "type": "generation_error",
                    "request_id": request_id,
                    "error": str(e)
                }))
            except:
                pass
            
            # Clean up
            if request_id in self.active_requests:
                del self.active_requests[request_id]
    
    def get_stage_name(self, progress):
        """Get stage name based on progress."""
        if progress < 25:
            return "initializing"
        elif progress < 50:
            return "processing_prompt"
        elif progress < 75:
            return "generating_latents"
        elif progress < 95:
            return "decoding_image"
        else:
            return "finalizing"
    
    async def handle_batch_generate(self, websocket, data):
        """Handle batch generation request."""
        batch_id = data.get("batch_id")
        batch_data = data.get("data", {})
        prompts = batch_data.get("prompts", [])
        
        logger.info(f"Batch generation request {batch_id} with {len(prompts)} prompts")
        
        # Send acknowledgment
        await websocket.send(json.dumps({
            "type": "batch_accepted",
            "batch_id": batch_id,
            "prompt_count": len(prompts),
            "estimated_time": len(prompts) * random.uniform(5, 10),
            "status": "queued"
        }))
        
        # Process each prompt
        for i, prompt in enumerate(prompts):
            request_id = str(uuid.uuid4())
            
            # Send batch progress
            await websocket.send(json.dumps({
                "type": "batch_progress",
                "batch_id": batch_id,
                "current": i + 1,
                "total": len(prompts),
                "current_request_id": request_id
            }))
            
            # Simulate individual generation
            await self.handle_generate_image(websocket, {
                "request_id": request_id,
                "data": prompt
            })
            
            # Wait a bit between prompts
            await asyncio.sleep(random.uniform(0.5, 1.0))
        
        # Send batch completion
        await websocket.send(json.dumps({
            "type": "batch_completed",
            "batch_id": batch_id,
            "total_processed": len(prompts),
            "status": "completed"
        }))
    
    async def handle_get_status(self, websocket, data):
        """Handle status request."""
        request_id = data.get("request_id")
        
        if request_id in self.active_requests:
            status = "processing"
            progress = random.randint(10, 90)
        elif request_id in self.completed_requests:
            status = "completed"
            progress = 100
        else:
            status = "not_found"
            progress = 0
        
        await websocket.send(json.dumps({
            "type": "status_response",
            "request_id": request_id,
            "status": status,
            "progress": progress
        }))
    
    async def handle_cancel_request(self, websocket, data):
        """Handle cancellation request."""
        request_id = data.get("request_id")
        
        if request_id in self.active_requests:
            del self.active_requests[request_id]
            status = "cancelled"
            message = "Request cancelled successfully"
        else:
            status = "not_found"
            message = "Request not found or already completed"
        
        await websocket.send(json.dumps({
            "type": "cancel_response",
            "request_id": request_id,
            "status": status,
            "message": message
        }))
    
    async def start(self):
        """Start the server."""
        logger.info(f"Starting mock Semantest server on ws://{self.host}:{self.port}/ws")
        
        async with websockets.serve(self.handle_client, self.host, self.port):
            logger.info("Server started. Press Ctrl+C to stop.")
            await asyncio.Future()  # Run forever


async def main():
    """Run the mock server."""
    server = MockSemantestServer()
    
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")


if __name__ == "__main__":
    print("🎭 Mock Semantest Server")
    print("========================")
    print("This server simulates Semantest for testing purposes.")
    print(f"WebSocket endpoint: ws://localhost:8080/ws")
    print("\nFeatures:")
    print("- Handshake protocol")
    print("- Single image generation with progress updates")
    print("- Batch processing")
    print("- Status queries")
    print("- Request cancellation")
    print("\nPress Ctrl+C to stop\n")
    
    asyncio.run(main())