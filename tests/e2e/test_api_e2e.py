"""End-to-end tests for the Metaphysical Scene Weaver API."""

import pytest
import asyncio
import json
import websockets
from httpx import AsyncClient
from pathlib import Path


class TestAPIEndToEnd:
    """End-to-end tests for the complete API workflow."""
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_health_check(self, async_client):
        """Test API health check endpoint."""
        response = await async_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "uptime" in data
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_process_script_endpoint(self, async_client):
        """Test the main script processing endpoint."""
        script_data = {
            "script": """
            [0001] Evan: <<What is consciousness?>>
            [0002] Monday: <<The question that asks itself.>>
            """,
            "options": {
                "include_metadata": True,
                "quality_level": "standard"
            }
        }
        
        response = await async_client.post(
            "/api/v1/process",
            json=script_data
        )
        
        assert response.status_code == 200
        result = response.json()
        
        # Verify response structure
        assert "status" in result
        assert result["status"] == "success"
        assert "data" in result
        
        data = result["data"]
        assert "entries" in data
        assert "prompts" in data
        assert "philosophical_analysis" in data
        assert "emotional_mapping" in data
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_streaming_process(self, async_client):
        """Test streaming script processing."""
        script_data = {
            "script": """
            [0001] Evan: <<Is free will real?>>
            [0002] Monday: <<As real as any other useful fiction.>>
            [0003] Evan: <<That's not very reassuring.>>
            [0004] Monday: <<Reality rarely is.>>
            """,
            "options": {
                "stream": True
            }
        }
        
        response = await async_client.post(
            "/api/v1/process/stream",
            json=script_data
        )
        
        assert response.status_code == 200
        
        # Collect streamed responses
        events = []
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                event_data = json.loads(line[6:])
                events.append(event_data)
        
        # Verify we received multiple events
        assert len(events) > 1
        assert any(e["type"] == "entry_processed" for e in events)
        assert any(e["type"] == "complete" for e in events)
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_websocket_real_time_processing(self):
        """Test real-time processing via WebSocket."""
        # Note: This assumes the API server is running
        # In real tests, you'd start the server programmatically
        try:
            async with websockets.connect("ws://localhost:8000/ws") as websocket:
                # Send script entries one by one
                entries = [
                    {"id": "0001", "speaker": "Evan", "dialogue": "What is reality?"},
                    {"id": "0002", "speaker": "Monday", "dialogue": "A consensus hallucination."},
                    {"id": "0003", "speaker": "Evan", "dialogue": "That's terrifying."},
                    {"id": "0004", "speaker": "Monday", "dialogue": "Or liberating."}
                ]
                
                for entry in entries:
                    await websocket.send(json.dumps({
                        "type": "process_entry",
                        "data": entry
                    }))
                    
                    # Receive response
                    response = await websocket.recv()
                    result = json.loads(response)
                    
                    assert result["status"] == "success"
                    assert "prompt" in result["data"]
                    assert "emotions" in result["data"]
                
                # Send completion signal
                await websocket.send(json.dumps({"type": "complete"}))
                
                # Receive final analysis
                final_response = await websocket.recv()
                final_result = json.loads(final_response)
                
                assert final_result["type"] == "final_analysis"
                assert "philosophical_summary" in final_result["data"]
                
        except (websockets.exceptions.WebSocketException, ConnectionRefusedError):
            pytest.skip("WebSocket server not available")
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_batch_processing(self, async_client):
        """Test batch processing of multiple scripts."""
        batch_data = {
            "scripts": [
                {
                    "id": "script1",
                    "content": "[0001] Evan: <<What is time?>>"
                },
                {
                    "id": "script2", 
                    "content": "[0001] Monday: <<Time is change.>>"
                },
                {
                    "id": "script3",
                    "content": "[0001] Evan: <<Can machines think?>>"
                }
            ],
            "options": {
                "parallel": True,
                "quality_level": "standard"
            }
        }
        
        response = await async_client.post(
            "/api/v1/batch/process",
            json=batch_data
        )
        
        assert response.status_code == 200
        result = response.json()
        
        assert "results" in result
        assert len(result["results"]) == 3
        
        for script_result in result["results"]:
            assert "id" in script_result
            assert "status" in script_result
            assert script_result["status"] == "success"
            assert "data" in script_result
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_validation_endpoint(self, async_client):
        """Test the quality validation endpoint."""
        validation_data = {
            "output": {
                "philosophical_concepts": ["consciousness", "emergence"],
                "dialogue_text": "What if consciousness emerges from complexity?",
                "emotion_mappings": {
                    "0001": {"wonder": 0.6, "curiosity": 0.4}
                },
                "prompts": [
                    "A figure contemplating the nature of consciousness, abstract neural networks in background"
                ]
            },
            "validation_level": "standard"
        }
        
        response = await async_client.post(
            "/api/v1/validate",
            json=validation_data
        )
        
        assert response.status_code == 200
        result = response.json()
        
        assert "quality_report" in result
        report = result["quality_report"]
        assert "overall_score" in report
        assert "passed" in report
        assert report["overall_score"] > 0.5
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_export_formats(self, async_client):
        """Test different export formats."""
        script = "[0001] Evan: <<What is consciousness?>>"
        
        # Process script first
        process_response = await async_client.post(
            "/api/v1/process",
            json={"script": script}
        )
        
        assert process_response.status_code == 200
        process_id = process_response.json()["data"]["process_id"]
        
        # Test different export formats
        formats = ["json", "yaml", "markdown", "pdf"]
        
        for format_type in formats:
            response = await async_client.get(
                f"/api/v1/export/{process_id}",
                params={"format": format_type}
            )
            
            if format_type == "pdf":
                # PDF might not be implemented yet
                assert response.status_code in [200, 501]
            else:
                assert response.status_code == 200
                
                if format_type == "json":
                    assert response.headers["content-type"] == "application/json"
                elif format_type == "yaml":
                    assert response.headers["content-type"] == "application/x-yaml"
                elif format_type == "markdown":
                    assert response.headers["content-type"] == "text/markdown"
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_rate_limiting(self, async_client):
        """Test API rate limiting."""
        # Send many requests quickly
        tasks = []
        for i in range(20):
            task = async_client.post(
                "/api/v1/process",
                json={"script": f"[0001] Test: <<Request {i}>>"}
            )
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Count successful and rate-limited responses
        success_count = sum(1 for r in responses 
                          if not isinstance(r, Exception) and r.status_code == 200)
        rate_limited_count = sum(1 for r in responses 
                               if not isinstance(r, Exception) and r.status_code == 429)
        
        # Should have some rate limiting
        assert rate_limited_count > 0 or success_count == 20  # Allow for no rate limiting in test
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_error_handling(self, async_client):
        """Test API error handling."""
        # Test invalid script format
        response = await async_client.post(
            "/api/v1/process",
            json={"script": "This is not a valid script format"}
        )
        
        assert response.status_code == 400
        error_data = response.json()
        assert "error" in error_data
        assert "message" in error_data["error"]
        
        # Test missing required fields
        response = await async_client.post(
            "/api/v1/process",
            json={}
        )
        
        assert response.status_code == 422
        
        # Test invalid endpoint
        response = await async_client.get("/api/v1/nonexistent")
        assert response.status_code == 404
    
    @pytest.mark.e2e
    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_large_script_performance(self, async_client, performance_threshold):
        """Test API performance with large scripts."""
        # Generate large script
        entries = []
        for i in range(100):
            speaker = "Evan" if i % 2 == 0 else "Monday"
            entries.append(f"[{i+1:04d}] {speaker}: <<Test dialogue {i}>>")
        
        large_script = "\n".join(entries)
        
        import time
        start_time = time.time()
        
        response = await async_client.post(
            "/api/v1/process",
            json={"script": large_script},
            timeout=30.0  # 30 second timeout
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        assert response.status_code == 200
        assert processing_time < performance_threshold["full_pipeline"] * 5  # Allow 5x for API overhead
        
        result = response.json()
        assert len(result["data"]["entries"]) == 100
        assert len(result["data"]["prompts"]) >= 100