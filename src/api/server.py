"""FastAPI server for real-time scene processing."""

from fastapi import FastAPI, HTTPException, WebSocket, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path
import json
import asyncio
import logging
import time
from datetime import datetime, timedelta
import jwt
from functools import lru_cache
from collections import defaultdict
import hashlib

from ..core.scene_weaver import SceneWeaver
from ..core.script_parser import ScriptParser, ScriptEntry

# Import routers
try:
    from .reality_effects import router as reality_router
    has_reality_effects = True
except ImportError:
    has_reality_effects = False
    logger = logging.getLogger(__name__)
    logger.warning("Reality effects module not available")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Metaphysical Scene Weaver API",
    description="Transform philosophical dialogue into visual narratives",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
if has_reality_effects:
    app.include_router(reality_router, prefix="/api")

# Security configuration
SECRET_KEY = "your-secret-key-here"  # TODO: Use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
security = HTTPBearer()

# Rate limiting configuration
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60  # seconds
rate_limit_storage = defaultdict(list)

# Cache configuration
CACHE_TTL = 300  # 5 minutes
cache_storage = {}


# Global scene weaver instance (initialized on startup)
scene_weaver: Optional[SceneWeaver] = None


# Authentication models
class TokenData(BaseModel):
    """Token data model."""
    username: str
    expires: datetime


class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Rate limiting decorator
def rate_limit(max_requests: int = RATE_LIMIT_REQUESTS, window: int = RATE_LIMIT_WINDOW):
    """Rate limiting decorator."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Get client IP or use a default identifier
            client_id = kwargs.get('client_id', 'default')
            current_time = time.time()
            
            # Clean old entries
            rate_limit_storage[client_id] = [
                timestamp for timestamp in rate_limit_storage[client_id]
                if current_time - timestamp < window
            ]
            
            # Check rate limit
            if len(rate_limit_storage[client_id]) >= max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Max {max_requests} requests per {window} seconds."
                )
            
            # Record request
            rate_limit_storage[client_id].append(current_time)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Caching decorator
def cache_response(ttl: int = CACHE_TTL):
    """Response caching decorator."""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = hashlib.md5(
                f"{func.__name__}_{str(args)}_{str(kwargs)}".encode()
            ).hexdigest()
            
            # Check cache
            if cache_key in cache_storage:
                cached_data, cached_time = cache_storage[cache_key]
                if time.time() - cached_time < ttl:
                    return cached_data
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Store in cache
            cache_storage[cache_key] = (result, time.time())
            
            return result
        return wrapper
    return decorator


# Authentication functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenData(username=username, expires=datetime.fromtimestamp(payload.get("exp")))
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Pydantic models
class ProcessRequest(BaseModel):
    """Request model for processing a single entry."""
    entry_id: str
    speaker: str
    dialogue: str
    panel_count: Optional[int] = None
    stage_directions: Optional[List[str]] = None
    metadata: Optional[List[str]] = None
    context_entries: Optional[List[Dict[str, Any]]] = None


class ProcessResponse(BaseModel):
    """Response model for processed scene."""
    entry_id: str
    prompt: str
    negative_prompt: str
    metadata: Dict[str, Any]
    philosophy: Dict[str, Any]
    emotion: Dict[str, Any]
    visual_elements: List[str]


class BatchProcessRequest(BaseModel):
    """Request model for batch processing."""
    entries: List[ProcessRequest]
    style: str = "comic book"


class ConfigUpdate(BaseModel):
    """Model for configuration updates."""
    philosophy_weight: Optional[float] = None
    emotion_weight: Optional[float] = None
    visual_weight: Optional[float] = None
    enable_metaphors: Optional[bool] = None
    max_prompt_length: Optional[int] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the scene weaver on startup."""
    global scene_weaver
    
    # Check for required files
    characters_path = Path("characters.json")
    places_path = Path("places.json")
    
    if not characters_path.exists() or not places_path.exists():
        logger.error("Required data files not found. Please ensure characters.json and places.json exist.")
        return
    
    try:
        scene_weaver = SceneWeaver(characters_path, places_path)
        logger.info("Scene Weaver initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Scene Weaver: {str(e)}")


@app.post("/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Login endpoint to get access token."""
    # TODO: Implement proper user authentication
    # This is a simple example - replace with real authentication
    if request.username == "admin" and request.password == "password":
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": request.username}, expires_delta=access_token_expires
        )
        return TokenResponse(
            access_token=access_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Metaphysical Scene Weaver API",
        "version": "0.1.0",
        "status": "ready" if scene_weaver else "not initialized",
        "endpoints": {
            "process": "/process",
            "batch": "/batch",
            "parse": "/parse",
            "config": "/config",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy" if scene_weaver else "unhealthy",
        "initialized": scene_weaver is not None
    }


@app.post("/process", response_model=ProcessResponse)
@rate_limit(max_requests=50, window=60)
@cache_response(ttl=300)
async def process_entry(request: ProcessRequest, token_data: TokenData = Depends(verify_token)):
    """Process a single script entry."""
    if not scene_weaver:
        raise HTTPException(status_code=503, detail="Scene Weaver not initialized")
    
    try:
        # Create ScriptEntry
        entry = ScriptEntry(
            id=request.entry_id,
            speaker=request.speaker,
            dialogue=request.dialogue,
            panel_count=request.panel_count,
            stage_directions=request.stage_directions or [],
            metadata=request.metadata or []
        )
        
        # Process with context if provided
        context_entries = []
        if request.context_entries:
            for ctx in request.context_entries:
                context_entries.append(ScriptEntry(
                    id=ctx['entry_id'],
                    speaker=ctx['speaker'],
                    dialogue=ctx['dialogue'],
                    panel_count=ctx.get('panel_count'),
                    stage_directions=ctx.get('stage_directions', []),
                    metadata=ctx.get('metadata', [])
                ))
        
        # Determine index (middle of context if provided)
        index = len(context_entries) // 2 if context_entries else 0
        all_entries = context_entries[:index] + [entry] + context_entries[index:]
        
        # Process the entry
        enriched_scene = scene_weaver.process_entry(entry, index, all_entries)
        
        # Generate negative prompt
        negative_prompt = scene_weaver.prompt_generator.generate_negative_prompt(
            {'scene_complexity': enriched_scene.metadata.get('visual_complexity', 'moderate')}
        )
        
        return ProcessResponse(
            entry_id=enriched_scene.entry_id,
            prompt=enriched_scene.prompt,
            negative_prompt=negative_prompt,
            metadata=enriched_scene.metadata,
            philosophy=enriched_scene.philosophy,
            emotion=enriched_scene.emotion,
            visual_elements=enriched_scene.visual_elements
        )
        
    except Exception as e:
        logger.error(f"Error processing entry: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch")
@rate_limit(max_requests=10, window=60)
async def batch_process(request: BatchProcessRequest, token_data: TokenData = Depends(verify_token)):
    """Process multiple entries as a batch."""
    if not scene_weaver:
        raise HTTPException(status_code=503, detail="Scene Weaver not initialized")
    
    try:
        # Update style if different
        if request.style != scene_weaver.prompt_generator.style.value:
            scene_weaver.prompt_generator.style = request.style
        
        # Convert to ScriptEntries
        entries = []
        for req_entry in request.entries:
            entries.append(ScriptEntry(
                id=req_entry.entry_id,
                speaker=req_entry.speaker,
                dialogue=req_entry.dialogue,
                panel_count=req_entry.panel_count,
                stage_directions=req_entry.stage_directions or [],
                metadata=req_entry.metadata or []
            ))
        
        # Process all entries
        results = []
        for i, entry in enumerate(entries):
            enriched_scene = scene_weaver.process_entry(entry, i, entries)
            
            results.append({
                'entry_id': enriched_scene.entry_id,
                'prompt': enriched_scene.prompt,
                'metadata': enriched_scene.metadata
            })
        
        return {"results": results, "total": len(results)}
        
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/parse")
@rate_limit(max_requests=100, window=60)
async def parse_text(text: str, token_data: TokenData = Depends(verify_token)):
    """Parse raw script text."""
    try:
        parser = ScriptParser()
        entries = parser.parse_text(text)
        
        return {
            "entries": [
                {
                    "id": entry.id,
                    "speaker": entry.speaker,
                    "dialogue": entry.dialogue,
                    "panel_count": entry.panel_count,
                    "stage_directions": entry.stage_directions,
                    "metadata": entry.metadata
                }
                for entry in entries
            ],
            "total": len(entries)
        }
        
    except Exception as e:
        logger.error(f"Error parsing text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/config")
@cache_response(ttl=60)
async def get_config(token_data: TokenData = Depends(verify_token)):
    """Get current configuration."""
    if not scene_weaver:
        raise HTTPException(status_code=503, detail="Scene Weaver not initialized")
    
    return scene_weaver.config


@app.put("/config")
async def update_config(update: ConfigUpdate, token_data: TokenData = Depends(verify_token)):
    """Update configuration."""
    # Clear cache when config changes
    cache_storage.clear()
    """Update configuration."""
    if not scene_weaver:
        raise HTTPException(status_code=503, detail="Scene Weaver not initialized")
    
    try:
        # Update only provided fields
        if update.philosophy_weight is not None:
            scene_weaver.config['philosophy_weight'] = update.philosophy_weight
        if update.emotion_weight is not None:
            scene_weaver.config['emotion_weight'] = update.emotion_weight
        if update.visual_weight is not None:
            scene_weaver.config['visual_weight'] = update.visual_weight
        if update.enable_metaphors is not None:
            scene_weaver.config['enable_metaphors'] = update.enable_metaphors
        if update.max_prompt_length is not None:
            scene_weaver.config['max_prompt_length'] = update.max_prompt_length
        
        return {"status": "updated", "config": scene_weaver.config}
        
    except Exception as e:
        logger.error(f"Error updating config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time processing."""
    await websocket.accept()
    
    # Simple WebSocket authentication
    try:
        # Wait for authentication message
        auth_data = await asyncio.wait_for(websocket.receive_json(), timeout=5.0)
        if auth_data.get("type") != "auth" or not auth_data.get("token"):
            await websocket.send_json({"error": "Authentication required"})
            await websocket.close()
            return
        
        # Verify token
        try:
            payload = jwt.decode(auth_data["token"], SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if not username:
                raise Exception("Invalid token")
        except:
            await websocket.send_json({"error": "Invalid authentication token"})
            await websocket.close()
            return
        
        await websocket.send_json({"type": "auth_success", "username": username})
        
    except asyncio.TimeoutError:
        await websocket.send_json({"error": "Authentication timeout"})
        await websocket.close()
        return
    
    if not scene_weaver:
        await websocket.send_json({"error": "Scene Weaver not initialized"})
        await websocket.close()
        return
    
    try:
        while True:
            # Receive data
            data = await websocket.receive_json()
            
            if data.get("type") == "process":
                # Process single entry
                entry = ScriptEntry(
                    id=data['entry_id'],
                    speaker=data['speaker'],
                    dialogue=data['dialogue'],
                    panel_count=data.get('panel_count'),
                    stage_directions=data.get('stage_directions', []),
                    metadata=data.get('metadata', [])
                )
                
                # Process
                enriched_scene = scene_weaver.process_entry(entry, 0, [entry])
                
                # Send response
                await websocket.send_json({
                    "type": "result",
                    "entry_id": enriched_scene.entry_id,
                    "prompt": enriched_scene.prompt,
                    "metadata": enriched_scene.metadata
                })
                
            elif data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
                
            elif data.get("type") == "close":
                break
                
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.send_json({"error": str(e)})
    finally:
        await websocket.close()


# Additional utility endpoints
@app.get("/stats")
@cache_response(ttl=30)
async def get_stats(token_data: TokenData = Depends(verify_token)):
    """Get API usage statistics."""
    return {
        "cache_size": len(cache_storage),
        "rate_limit_clients": len(rate_limit_storage),
        "scene_weaver_initialized": scene_weaver is not None,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/cache/clear")
async def clear_cache(token_data: TokenData = Depends(verify_token)):
    """Clear response cache."""
    cache_storage.clear()
    return {"status": "cache cleared", "timestamp": datetime.utcnow().isoformat()}


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "Not found", "path": str(request.url.path)}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )