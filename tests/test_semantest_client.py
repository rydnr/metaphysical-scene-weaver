"""Tests for Semantest integration client with mock WebSocket server."""

import asyncio
import json
import pytest
import websockets
from unittest.mock import Mock, AsyncMock, patch
from websockets.exceptions import WebSocketException
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from integrations.semantest_client import SemantestClient, SemantestConfig, SemantestIntegration
from core.scene_weaver import ScriptEntry


class MockWebSocketServer:
    """Mock WebSocket server for testing."""
    
    def __init__(self, port=8765):
        self.port = port
        self.messages_received = []
        self.server = None
        self.clients = set()
        self.response_queue = asyncio.Queue()
        
    async def handler(self, websocket, path):
        """Handle WebSocket connections."""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                self.messages_received.append(data)
                
                # Handle different message types
                if data.get("type") == "handshake":
                    await websocket.send(json.dumps({
                        "type": "handshake_ack",
                        "server": "mock_semantest",
                        "version": "0.1.0"
                    }))
                    
                elif data.get("type") == "generate_image":
                    # Simulate processing
                    request_id = data.get("request_id")
                    
                    # Send progress updates
                    for progress in [25, 50, 75, 100]:
                        await asyncio.sleep(0.1)
                        await websocket.send(json.dumps({
                            "type": "progress_update",
                            "request_id": request_id,
                            "progress": progress
                        }))
                    
                    # Send completion
                    await websocket.send(json.dumps({
                        "type": "image_ready",
                        "request_id": request_id,
                        "image_url": f"http://mock.semantest.com/images/{request_id}.png"
                    }))
                    
                elif data.get("type") == "batch_generate":
                    batch_id = data.get("batch_id")
                    await websocket.send(json.dumps({
                        "type": "batch_accepted",
                        "batch_id": batch_id,
                        "status": "processing"
                    }))
                    
                elif data.get("type") == "get_status":
                    request_id = data.get("request_id")
                    await websocket.send(json.dumps({
                        "type": "status_response",
                        "request_id": request_id,
                        "status": "processing",
                        "progress": 50
                    }))
                    
                # Check if there are queued responses
                if not self.response_queue.empty():
                    response = await self.response_queue.get()
                    await websocket.send(json.dumps(response))
                    
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            self.clients.remove(websocket)
    
    async def start(self):
        """Start the mock server."""
        self.server = await websockets.serve(self.handler, "localhost", self.port)
        
    async def stop(self):
        """Stop the mock server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            
    async def send_error(self, request_id: str, error_message: str):
        """Queue an error response."""
        await self.response_queue.put({
            "type": "generation_error",
            "request_id": request_id,
            "error": error_message
        })


@pytest.fixture
async def mock_server():
    """Create and start a mock WebSocket server."""
    server = MockWebSocketServer()
    await server.start()
    yield server
    await server.stop()


@pytest.fixture
def client_config():
    """Create test client configuration."""
    return SemantestConfig(
        websocket_url="ws://localhost:8765/ws",
        api_key="test_api_key",
        reconnect_interval=1,
        max_reconnect_attempts=3
    )


class TestSemantestClient:
    """Test cases for SemantestClient."""
    
    @pytest.mark.asyncio
    async def test_connect_success(self, mock_server, client_config):
        """Test successful connection to server."""
        client = SemantestClient(client_config)
        
        # Connect
        connected = await client.connect()
        assert connected is True
        assert client.is_connected is True
        assert client.websocket is not None
        
        # Check handshake was sent
        await asyncio.sleep(0.1)  # Allow time for handshake
        assert len(mock_server.messages_received) == 1
        assert mock_server.messages_received[0]["type"] == "handshake"
        
        # Disconnect
        await client.disconnect()
        assert client.is_connected is False
    
    @pytest.mark.asyncio
    async def test_connect_failure(self):
        """Test connection failure handling."""
        config = SemantestConfig(websocket_url="ws://localhost:9999/ws")
        client = SemantestClient(config)
        
        connected = await client.connect()
        assert connected is False
        assert client.is_connected is False
        assert client.websocket is None
    
    @pytest.mark.asyncio
    async def test_send_prompt(self, mock_server, client_config):
        """Test sending a prompt for image generation."""
        client = SemantestClient(client_config)
        await client.connect()
        
        # Send prompt
        prompt_data = {
            "prompt": "A philosophical scene with deep meaning",
            "negative_prompt": "low quality, blurry",
            "width": 1024,
            "height": 768,
            "steps": 30,
            "guidance_scale": 7.5,
            "style": "comic book"
        }
        
        request_id = await client.send_prompt(prompt_data)
        assert request_id is not None
        
        # Check message was sent
        await asyncio.sleep(0.1)
        assert len(mock_server.messages_received) == 2  # handshake + prompt
        prompt_msg = mock_server.messages_received[1]
        assert prompt_msg["type"] == "generate_image"
        assert prompt_msg["request_id"] == request_id
        assert prompt_msg["data"]["prompt"] == prompt_data["prompt"]
        
        await client.disconnect()
    
    @pytest.mark.asyncio
    async def test_send_batch(self, mock_server, client_config):
        """Test sending a batch of prompts."""
        client = SemantestClient(client_config)
        await client.connect()
        
        # Prepare batch
        prompts = [
            {"prompt": "Scene 1", "entry_id": "001"},
            {"prompt": "Scene 2", "entry_id": "002"},
            {"prompt": "Scene 3", "entry_id": "003"}
        ]
        
        batch_id = await client.send_batch(prompts)
        assert batch_id is not None
        
        # Check message
        await asyncio.sleep(0.1)
        batch_msg = mock_server.messages_received[-1]
        assert batch_msg["type"] == "batch_generate"
        assert batch_msg["batch_id"] == batch_id
        assert len(batch_msg["data"]["prompts"]) == 3
        
        await client.disconnect()
    
    @pytest.mark.asyncio
    async def test_message_handlers(self, mock_server, client_config):
        """Test message handler registration and execution."""
        client = SemantestClient(client_config)
        await client.connect()
        
        # Track handled messages
        handled_messages = []
        
        async def handle_image_ready(data):
            handled_messages.append(("image_ready", data))
        
        async def handle_progress(data):
            handled_messages.append(("progress", data))
        
        # Register handlers
        client.on_message("image_ready", handle_image_ready)
        client.on_message("progress_update", handle_progress)
        
        # Start listening
        listen_task = asyncio.create_task(client.listen())
        
        # Send a prompt to trigger responses
        await client.send_prompt({"prompt": "Test scene"})
        
        # Wait for messages to be handled
        await asyncio.sleep(0.5)
        
        # Check handlers were called
        assert len(handled_messages) > 0
        assert any(msg[0] == "progress" for msg in handled_messages)
        assert any(msg[0] == "image_ready" for msg in handled_messages)
        
        # Stop listening
        client._running = False
        await client.disconnect()
        listen_task.cancel()
        try:
            await listen_task
        except asyncio.CancelledError:
            pass
    
    @pytest.mark.asyncio
    async def test_reconnection(self, client_config):
        """Test automatic reconnection logic."""
        client = SemantestClient(client_config)
        
        # Mock websocket that fails then succeeds
        connect_attempts = 0
        
        async def mock_connect(*args, **kwargs):
            nonlocal connect_attempts
            connect_attempts += 1
            if connect_attempts < 3:
                raise ConnectionError("Mock connection failure")
            
            # Create a mock websocket
            mock_ws = AsyncMock()
            mock_ws.recv = AsyncMock(side_effect=WebSocketException("Connection closed"))
            mock_ws.send = AsyncMock()
            return mock_ws
        
        with patch('websockets.connect', mock_connect):
            # Start listening (will attempt reconnection)
            listen_task = asyncio.create_task(client.listen())
            
            # Let it try to reconnect
            await asyncio.sleep(3)
            
            # Check reconnection attempts were made
            assert connect_attempts >= 2
            
            # Stop
            client._running = False
            listen_task.cancel()
            try:
                await listen_task
            except asyncio.CancelledError:
                pass
    
    @pytest.mark.asyncio
    async def test_connection_not_established(self, client_config):
        """Test operations when not connected."""
        client = SemantestClient(client_config)
        
        # Try to send without connecting
        with pytest.raises(ConnectionError):
            await client.send_prompt({"prompt": "test"})
        
        with pytest.raises(ConnectionError):
            await client.send_batch([])
        
        with pytest.raises(ConnectionError):
            await client.get_status("test_id")


class TestSemantestIntegration:
    """Test cases for SemantestIntegration."""
    
    @pytest.mark.asyncio
    async def test_integration_start(self, mock_server, client_config):
        """Test starting the integration."""
        # Mock SceneWeaver
        mock_scene_weaver = Mock()
        
        integration = SemantestIntegration(mock_scene_weaver, client_config)
        
        # Start integration
        started = await integration.start()
        assert started is True
        assert integration.client.is_connected is True
        
        # Check handlers were registered
        assert "image_ready" in integration.client.message_handlers
        assert "generation_error" in integration.client.message_handlers
        assert "progress_update" in integration.client.message_handlers
        
        # Stop
        await integration.client.disconnect()
    
    @pytest.mark.asyncio
    async def test_process_and_generate(self, mock_server, client_config):
        """Test processing a script entry and generating image."""
        # Create mock objects
        mock_scene_weaver = Mock()
        mock_enriched_scene = Mock()
        mock_enriched_scene.prompt = "A philosophical scene"
        mock_enriched_scene.entry_id = "test_001"
        mock_enriched_scene.metadata = {
            "visual_complexity": "high",
            "speaker": "Narrator",
            "panel_count": 1
        }
        mock_enriched_scene.philosophy = {"primary_concept": "existentialism"}
        mock_enriched_scene.emotion = {"primary": "contemplative"}
        
        mock_scene_weaver.process_entry.return_value = mock_enriched_scene
        mock_scene_weaver.prompt_generator.generate_negative_prompt.return_value = "low quality"
        mock_scene_weaver.prompt_generator.style.value = "comic book"
        
        # Create integration
        integration = SemantestIntegration(mock_scene_weaver, client_config)
        await integration.start()
        
        # Create script entry
        script_entry = Mock()
        script_entry.entry_id = "test_001"
        
        # Process and generate
        request_id = await integration.process_and_generate(script_entry)
        assert request_id is not None
        
        # Check tracking
        assert request_id in integration.pending_requests
        assert integration.pending_requests[request_id]["entry_id"] == "test_001"
        assert integration.pending_requests[request_id]["status"] == "pending"
        
        # Stop
        await integration.client.disconnect()
    
    @pytest.mark.asyncio
    async def test_handle_image_ready(self, mock_server, client_config):
        """Test handling image ready notification."""
        mock_scene_weaver = Mock()
        integration = SemantestIntegration(mock_scene_weaver, client_config)
        
        # Add a pending request
        request_id = "test_request_123"
        integration.pending_requests[request_id] = {
            "entry_id": "test_001",
            "status": "pending"
        }
        
        # Handle image ready
        await integration._handle_image_ready({
            "request_id": request_id,
            "image_url": "http://example.com/image.png"
        })
        
        # Check status updated
        assert integration.pending_requests[request_id]["status"] == "completed"
        assert integration.pending_requests[request_id]["image_url"] == "http://example.com/image.png"
    
    @pytest.mark.asyncio
    async def test_handle_generation_error(self, mock_server, client_config):
        """Test handling generation errors."""
        mock_scene_weaver = Mock()
        integration = SemantestIntegration(mock_scene_weaver, client_config)
        
        # Add a pending request
        request_id = "test_request_456"
        integration.pending_requests[request_id] = {
            "entry_id": "test_002",
            "status": "pending"
        }
        
        # Handle error
        await integration._handle_generation_error({
            "request_id": request_id,
            "error": "GPU out of memory"
        })
        
        # Check status updated
        assert integration.pending_requests[request_id]["status"] == "error"
        assert integration.pending_requests[request_id]["error"] == "GPU out of memory"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])