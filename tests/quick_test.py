#!/usr/bin/env python3
"""Quick test to verify Semantest client works."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from integrations.semantest_client import SemantestClient, SemantestConfig


async def quick_test():
    """Run a quick connection test."""
    print("🧪 Quick Semantest Client Test")
    print("==============================\n")
    
    # Test 1: Connection
    print("1. Testing connection...")
    config = SemantestConfig(
        websocket_url="ws://localhost:8080/ws",
        reconnect_interval=1,
        max_reconnect_attempts=2
    )
    
    client = SemantestClient(config)
    
    try:
        connected = await client.connect()
        if connected:
            print("   ✅ Connected successfully!")
            
            # Test 2: Send prompt
            print("\n2. Testing prompt sending...")
            request_id = await client.send_prompt({
                "prompt": "A test scene",
                "style": "comic book"
            })
            print(f"   ✅ Prompt sent! Request ID: {request_id}")
            
            # Test 3: Message handling
            print("\n3. Testing message reception...")
            messages_received = []
            
            async def track_messages(data):
                messages_received.append(data)
                print(f"   📨 Received: {data.get('type')}")
            
            # Register handler for all message types
            client.on_message("progress_update", track_messages)
            client.on_message("image_ready", track_messages)
            
            # Listen for a few seconds
            listen_task = asyncio.create_task(client.listen())
            await asyncio.sleep(3)
            
            print(f"   ✅ Received {len(messages_received)} messages")
            
            # Clean up
            client._running = False
            listen_task.cancel()
            await client.disconnect()
            
            print("\n✅ All tests passed!")
            
        else:
            print("   ❌ Connection failed!")
            print("   Make sure the mock server is running:")
            print("   python tests/mock_semantest_server.py")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("\n   To run this test:")
        print("   1. Start mock server: python tests/mock_semantest_server.py")
        print("   2. Run this test: python tests/quick_test.py")


if __name__ == "__main__":
    asyncio.run(quick_test())