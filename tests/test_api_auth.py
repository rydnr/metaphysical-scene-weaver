#!/usr/bin/env python3
"""Test script for API authentication and rate limiting."""

import asyncio
import aiohttp
import json
import time
from typing import Optional


class APITestClient:
    """Test client for the Metaphysical Scene Weaver API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token: Optional[str] = None
        
    async def login(self, username: str, password: str):
        """Login and get access token."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    self.token = data["access_token"]
                    print(f"✅ Login successful! Token expires in {data['expires_in']} seconds")
                    return True
                else:
                    print(f"❌ Login failed: {response.status}")
                    return False
    
    async def test_endpoint(self, endpoint: str, method: str = "GET", data: Optional[dict] = None):
        """Test an authenticated endpoint."""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        async with aiohttp.ClientSession() as session:
            kwargs = {"headers": headers}
            if data and method != "GET":
                kwargs["json"] = data
                
            async with session.request(method, f"{self.base_url}{endpoint}", **kwargs) as response:
                return response.status, await response.json()
    
    async def test_rate_limiting(self):
        """Test rate limiting."""
        print("\n🔒 Testing Rate Limiting")
        print("=" * 40)
        
        # Try to exceed rate limit for /process endpoint (50 requests per 60 seconds)
        success_count = 0
        rate_limited_count = 0
        
        print("Sending 60 requests to /process endpoint...")
        
        for i in range(60):
            status, data = await self.test_endpoint(
                "/process",
                "POST",
                {
                    "entry_id": f"test_{i}",
                    "speaker": "Test",
                    "dialogue": f"Test dialogue {i}"
                }
            )
            
            if status == 200:
                success_count += 1
            elif status == 429:
                rate_limited_count += 1
                print(f"  Rate limited at request {i+1}: {data.get('detail', 'Unknown')}")
            
            # Small delay to avoid overwhelming the server
            await asyncio.sleep(0.1)
        
        print(f"\n📊 Results:")
        print(f"  Successful: {success_count}")
        print(f"  Rate limited: {rate_limited_count}")
        
    async def test_cache(self):
        """Test response caching."""
        print("\n💾 Testing Response Cache")
        print("=" * 40)
        
        # Make same request multiple times
        print("Making 5 identical requests to /config...")
        
        times = []
        for i in range(5):
            start = time.time()
            status, data = await self.test_endpoint("/config")
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"  Request {i+1}: {elapsed:.3f}s - Status: {status}")
            await asyncio.sleep(0.5)
        
        # First request should be slower than cached ones
        avg_first = times[0]
        avg_cached = sum(times[1:]) / len(times[1:])
        
        print(f"\n📊 Cache Performance:")
        print(f"  First request: {avg_first:.3f}s")
        print(f"  Cached requests (avg): {avg_cached:.3f}s")
        print(f"  Speed improvement: {(avg_first/avg_cached - 1) * 100:.1f}%")
    
    async def test_websocket_auth(self):
        """Test WebSocket authentication."""
        print("\n🔌 Testing WebSocket Authentication")
        print("=" * 40)
        
        import websockets
        
        try:
            async with websockets.connect(f"ws://localhost:8000/ws") as websocket:
                # Test without authentication
                print("1. Testing without authentication...")
                await asyncio.sleep(6)  # Wait for timeout
                
        except websockets.exceptions.ConnectionClosed:
            print("   ✅ Connection closed as expected (no auth)")
        
        try:
            async with websockets.connect(f"ws://localhost:8000/ws") as websocket:
                # Test with authentication
                print("\n2. Testing with authentication...")
                await websocket.send(json.dumps({
                    "type": "auth",
                    "token": self.token
                }))
                
                response = await websocket.recv()
                data = json.loads(response)
                
                if data.get("type") == "auth_success":
                    print(f"   ✅ Authentication successful! User: {data.get('username')}")
                    
                    # Test processing
                    await websocket.send(json.dumps({
                        "type": "process",
                        "entry_id": "ws_test_001",
                        "speaker": "WebSocket Test",
                        "dialogue": "Testing WebSocket processing"
                    }))
                    
                    result = await websocket.recv()
                    result_data = json.loads(result)
                    if result_data.get("type") == "result":
                        print("   ✅ WebSocket processing successful!")
                else:
                    print(f"   ❌ Authentication failed: {data}")
                    
        except Exception as e:
            print(f"   ❌ WebSocket error: {e}")


async def main():
    """Run all API tests."""
    print("🧪 Metaphysical Scene Weaver API Tests")
    print("=====================================")
    print("Note: Make sure the API server is running at http://localhost:8000")
    print("      Start it with: uvicorn src.api.server:app --reload\n")
    
    client = APITestClient()
    
    # Test 1: Authentication
    print("🔐 Testing Authentication")
    print("=" * 40)
    
    # Test invalid credentials
    print("1. Testing invalid credentials...")
    success = await client.login("wrong", "credentials")
    if not success:
        print("   ✅ Invalid credentials rejected")
    
    # Test valid credentials
    print("\n2. Testing valid credentials...")
    success = await client.login("admin", "password")
    if success:
        print("   ✅ Valid credentials accepted")
    else:
        print("   ❌ Failed to login with valid credentials")
        return
    
    # Test 2: Protected endpoints
    print("\n🛡️ Testing Protected Endpoints")
    print("=" * 40)
    
    endpoints = ["/config", "/stats", "/health"]
    for endpoint in endpoints:
        status, data = await client.test_endpoint(endpoint)
        print(f"{endpoint}: Status {status} - {'✅ Authorized' if status == 200 else '❌ Unauthorized'}")
    
    # Test 3: Rate limiting
    await client.test_rate_limiting()
    
    # Test 4: Caching
    await client.test_cache()
    
    # Test 5: WebSocket authentication
    await client.test_websocket_auth()
    
    print("\n✨ All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())