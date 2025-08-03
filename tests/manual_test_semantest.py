"""Manual test runner for Semantest client without pytest."""

import asyncio
import json
import logging
import sys
from pathlib import Path
from unittest.mock import Mock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from integrations.semantest_client import SemantestClient, SemantestConfig

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


async def test_basic_connection():
    """Test basic connection functionality."""
    print("\n=== Testing Basic Connection ===")
    
    config = SemantestConfig(
        websocket_url="ws://localhost:8080/ws",  # Default Semantest URL
        api_key="test_api_key",
        reconnect_interval=2,
        max_reconnect_attempts=3
    )
    
    client = SemantestClient(config)
    
    # Try to connect
    print("Attempting to connect...")
    connected = await client.connect()
    
    if connected:
        print("✅ Connection successful!")
        
        # Test sending a prompt
        print("\nTesting prompt sending...")
        try:
            prompt_data = {
                "prompt": "A philosophical scene depicting the nature of consciousness",
                "negative_prompt": "low quality, blurry, distorted",
                "width": 1024,
                "height": 1024,
                "steps": 30,
                "guidance_scale": 7.5,
                "seed": 42,
                "style": "comic book"
            }
            
            request_id = await client.send_prompt(prompt_data)
            print(f"✅ Prompt sent successfully! Request ID: {request_id}")
            
        except Exception as e:
            print(f"❌ Failed to send prompt: {e}")
        
        # Disconnect
        await client.disconnect()
        print("✅ Disconnected successfully")
        
    else:
        print("❌ Connection failed - is Semantest running?")
        print("   To start a mock server, run: python tests/mock_semantest_server.py")


async def test_message_handling():
    """Test message handling with callbacks."""
    print("\n=== Testing Message Handling ===")
    
    config = SemantestConfig(websocket_url="ws://localhost:8080/ws")
    client = SemantestClient(config)
    
    # Set up message handlers
    received_messages = []
    
    async def handle_image_ready(data):
        print(f"📸 Image ready: {data.get('image_url')}")
        received_messages.append(("image_ready", data))
    
    async def handle_progress(data):
        print(f"⏳ Progress: {data.get('progress')}%")
        received_messages.append(("progress", data))
    
    async def handle_error(data):
        print(f"❌ Error: {data.get('error')}")
        received_messages.append(("error", data))
    
    # Register handlers
    client.on_message("image_ready", handle_image_ready)
    client.on_message("progress_update", handle_progress)
    client.on_message("generation_error", handle_error)
    
    # Connect
    if await client.connect():
        print("✅ Connected, starting listener...")
        
        # Start listening in background
        listen_task = asyncio.create_task(client.listen())
        
        # Send a test prompt
        try:
            request_id = await client.send_prompt({
                "prompt": "Test scene for message handling",
                "style": "comic book"
            })
            print(f"📤 Sent prompt: {request_id}")
            
            # Wait for responses
            print("⏳ Waiting for responses (10 seconds)...")
            await asyncio.sleep(10)
            
            print(f"\n📊 Received {len(received_messages)} messages")
            
        except Exception as e:
            print(f"❌ Error during test: {e}")
        
        # Clean up
        client._running = False
        await client.disconnect()
        listen_task.cancel()
        try:
            await listen_task
        except asyncio.CancelledError:
            pass
    else:
        print("❌ Failed to connect")


async def test_batch_processing():
    """Test batch processing functionality."""
    print("\n=== Testing Batch Processing ===")
    
    config = SemantestConfig(websocket_url="ws://localhost:8080/ws")
    client = SemantestClient(config)
    
    if await client.connect():
        print("✅ Connected")
        
        # Prepare batch
        prompts = [
            {
                "entry_id": "scene_001",
                "prompt": "Opening scene: A vast cosmic void",
                "style": "comic book",
                "metadata": {"panel": 1, "chapter": 1}
            },
            {
                "entry_id": "scene_002", 
                "prompt": "A lone figure contemplates existence",
                "style": "comic book",
                "metadata": {"panel": 2, "chapter": 1}
            },
            {
                "entry_id": "scene_003",
                "prompt": "Reality fractures into infinite possibilities",
                "style": "comic book",
                "metadata": {"panel": 3, "chapter": 1}
            }
        ]
        
        try:
            batch_id = await client.send_batch(prompts)
            print(f"✅ Batch sent successfully! Batch ID: {batch_id}")
            print(f"   Contains {len(prompts)} prompts")
            
        except Exception as e:
            print(f"❌ Failed to send batch: {e}")
        
        await client.disconnect()
    else:
        print("❌ Failed to connect")


async def test_reconnection():
    """Test reconnection behavior."""
    print("\n=== Testing Reconnection ===")
    
    config = SemantestConfig(
        websocket_url="ws://localhost:8080/ws",
        reconnect_interval=2,
        max_reconnect_attempts=3
    )
    
    client = SemantestClient(config)
    
    print("Starting listener (will attempt reconnections)...")
    print("Press Ctrl+C to stop")
    
    # This will automatically try to connect and reconnect
    try:
        await client.listen()
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Listener stopped: {e}")


async def main():
    """Run all tests."""
    print("🧪 Semantest Client Manual Tests")
    print("================================")
    print("Note: These tests expect a Semantest server at ws://localhost:8080/ws")
    print("      You can start the mock server with: python tests/mock_semantest_server.py\n")
    
    # Run tests
    await test_basic_connection()
    await test_message_handling()
    await test_batch_processing()
    await test_reconnection()
    
    print("\n✨ Tests completed!")


if __name__ == "__main__":
    asyncio.run(main())