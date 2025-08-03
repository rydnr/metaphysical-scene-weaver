# Metaphysical Scene Weaver API Guide

## Overview

The Metaphysical Scene Weaver provides a FastAPI-based REST API and WebSocket interface for real-time philosophical scene processing and image generation.

## Features

- **JWT Authentication**: Secure API access with token-based authentication
- **Rate Limiting**: Prevent API abuse with configurable rate limits
- **Response Caching**: Improved performance with intelligent caching
- **WebSocket Support**: Real-time bidirectional communication
- **Batch Processing**: Efficient handling of multiple scenes
- **CORS Support**: Cross-origin resource sharing for web clients
- **Monitoring**: Built-in stats and metrics endpoints

## Getting Started

### Installation

```bash
# Install dependencies
pip install -e .

# Start the API server
uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000
```

### Authentication

All API endpoints (except `/health` and `/`) require authentication. 

1. **Login to get access token:**

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

2. **Use token in requests:**

```bash
curl -X GET "http://localhost:8000/config" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## API Endpoints

### Authentication

#### POST `/auth/login`
Login and receive access token.

**Request Body:**
```json
{
  "username": "admin",
  "password": "password"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Scene Processing

#### POST `/process`
Process a single script entry into a visual scene.

**Rate Limit:** 50 requests per minute  
**Cache:** 5 minutes

**Request Body:**
```json
{
  "entry_id": "scene_001",
  "speaker": "Narrator",
  "dialogue": "The universe unfolds before us...",
  "panel_count": 1,
  "stage_directions": ["Wide shot", "Cosmic setting"],
  "metadata": ["philosophical", "contemplative"],
  "context_entries": []
}
```

**Response:**
```json
{
  "entry_id": "scene_001",
  "prompt": "A vast cosmic panorama...",
  "negative_prompt": "low quality, blurry...",
  "metadata": {
    "visual_complexity": "high",
    "panel_layout": "single"
  },
  "philosophy": {
    "primary_concept": "existentialism",
    "secondary_concepts": ["consciousness", "infinity"]
  },
  "emotion": {
    "primary": "awe",
    "intensity": 0.8
  },
  "visual_elements": ["stars", "nebulae", "vast space"]
}
```

#### POST `/batch`
Process multiple entries in a single request.

**Rate Limit:** 10 requests per minute

**Request Body:**
```json
{
  "entries": [
    {
      "entry_id": "scene_001",
      "speaker": "Narrator",
      "dialogue": "First scene..."
    },
    {
      "entry_id": "scene_002",
      "speaker": "Character",
      "dialogue": "Second scene..."
    }
  ],
  "style": "comic book"
}
```

### Script Parsing

#### POST `/parse`
Parse raw script text into structured entries.

**Rate Limit:** 100 requests per minute

**Request Body:**
```text
NARRATOR: The story begins...
[Wide shot of cosmic void]

CHARACTER: Where are we?
```

**Response:**
```json
{
  "entries": [
    {
      "id": "001",
      "speaker": "NARRATOR",
      "dialogue": "The story begins...",
      "stage_directions": ["Wide shot of cosmic void"]
    }
  ],
  "total": 1
}
```

### Configuration

#### GET `/config`
Get current scene weaver configuration.

**Cache:** 1 minute

**Response:**
```json
{
  "philosophy_weight": 0.3,
  "emotion_weight": 0.3,
  "visual_weight": 0.4,
  "enable_metaphors": true,
  "max_prompt_length": 500
}
```

#### PUT `/config`
Update configuration settings.

**Note:** Clears response cache

**Request Body:**
```json
{
  "philosophy_weight": 0.4,
  "emotion_weight": 0.3,
  "visual_weight": 0.3
}
```

### Monitoring

#### GET `/health`
Health check endpoint (no authentication required).

**Response:**
```json
{
  "status": "healthy",
  "initialized": true
}
```

#### GET `/stats`
Get API usage statistics.

**Cache:** 30 seconds

**Response:**
```json
{
  "cache_size": 42,
  "rate_limit_clients": 5,
  "scene_weaver_initialized": true,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### POST `/cache/clear`
Clear the response cache.

**Response:**
```json
{
  "status": "cache cleared",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## WebSocket Interface

### Connection

Connect to `ws://localhost:8000/ws`

### Authentication Flow

1. **Send authentication message within 5 seconds:**
```json
{
  "type": "auth",
  "token": "YOUR_ACCESS_TOKEN"
}
```

2. **Receive authentication response:**
```json
{
  "type": "auth_success",
  "username": "admin"
}
```

### Message Types

#### Process Entry
```json
{
  "type": "process",
  "entry_id": "ws_001",
  "speaker": "Narrator",
  "dialogue": "The scene unfolds...",
  "panel_count": 1
}
```

#### Receive Result
```json
{
  "type": "result",
  "entry_id": "ws_001",
  "prompt": "Generated prompt...",
  "metadata": {}
}
```

#### Heartbeat
```json
{
  "type": "ping"
}
```

Response:
```json
{
  "type": "pong"
}
```

## Rate Limiting

Rate limits are applied per client (IP address):

| Endpoint | Limit | Window |
|----------|-------|---------|
| `/process` | 50 | 60 seconds |
| `/batch` | 10 | 60 seconds |
| `/parse` | 100 | 60 seconds |

When rate limited, the API returns:
```json
{
  "detail": "Rate limit exceeded. Max 50 requests per 60 seconds."
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 429 Too Many Requests
```json
{
  "detail": "Rate limit exceeded"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

### 503 Service Unavailable
```json
{
  "detail": "Scene Weaver not initialized"
}
```

## Python Client Example

```python
import aiohttp
import asyncio

class SceneWeaverClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.token = None
    
    async def login(self, username, password):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/auth/login",
                json={"username": username, "password": password}
            ) as resp:
                data = await resp.json()
                self.token = data["access_token"]
    
    async def process_scene(self, dialogue, speaker="Narrator"):
        headers = {"Authorization": f"Bearer {self.token}"}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/process",
                headers=headers,
                json={
                    "entry_id": "test_001",
                    "speaker": speaker,
                    "dialogue": dialogue
                }
            ) as resp:
                return await resp.json()

# Usage
async def main():
    client = SceneWeaverClient()
    await client.login("admin", "password")
    result = await client.process_scene("The universe speaks...")
    print(result)

asyncio.run(main())
```

## Configuration

### Environment Variables

Set these in your `.env` file:

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Security
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Cache
CACHE_TTL=300

# CORS
ALLOWED_ORIGINS=http://localhost:3000,https://example.com
```

### Production Deployment

For production deployment:

1. **Use environment variables for secrets**
2. **Configure CORS properly** (don't use `*`)
3. **Set up HTTPS** with SSL certificates
4. **Use a proper database** for user management
5. **Configure logging** and monitoring
6. **Set up rate limiting** per user, not just IP
7. **Use Redis** for distributed caching and rate limiting

## Testing

Run the test scripts:

```bash
# Test authentication and rate limiting
python tests/test_api_auth.py

# Test with mock Semantest server
python tests/mock_semantest_server.py
python tests/test_semantest_client.py
```

## Performance Tips

1. **Enable caching** for frequently accessed data
2. **Use batch processing** for multiple scenes
3. **Implement client-side caching** of tokens
4. **Use WebSocket** for real-time requirements
5. **Monitor rate limits** and adjust as needed

## Security Best Practices

1. **Never expose** the SECRET_KEY
2. **Use HTTPS** in production
3. **Implement proper** user authentication
4. **Validate all inputs** 
5. **Log security events**
6. **Regular security audits**
7. **Keep dependencies updated**