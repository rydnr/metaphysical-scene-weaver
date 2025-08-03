"""Robust WebSocket handler with connection management and error recovery."""

import asyncio
import json
import logging
from typing import Dict, Any, Optional, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import websockets
from websockets.exceptions import WebSocketException, ConnectionClosed
from collections import defaultdict
import time


class ConnectionState(Enum):
    """WebSocket connection states."""
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    RECONNECTING = "reconnecting"
    FAILED = "failed"


@dataclass
class ConnectionMetrics:
    """Metrics for connection monitoring."""
    connect_time: Optional[datetime] = None
    disconnect_time: Optional[datetime] = None
    messages_sent: int = 0
    messages_received: int = 0
    errors_count: int = 0
    reconnect_attempts: int = 0
    bytes_sent: int = 0
    bytes_received: int = 0
    
    def reset(self):
        """Reset metrics for new connection."""
        self.connect_time = datetime.utcnow()
        self.disconnect_time = None
        self.messages_sent = 0
        self.messages_received = 0
        self.errors_count = 0
        self.bytes_sent = 0
        self.bytes_received = 0


@dataclass
class WebSocketConfig:
    """Configuration for WebSocket handler."""
    url: str
    reconnect_interval: float = 5.0
    max_reconnect_attempts: int = 10
    heartbeat_interval: float = 30.0
    message_timeout: float = 60.0
    max_message_size: int = 10 * 1024 * 1024  # 10MB
    compression: Optional[str] = "deflate"
    extra_headers: Dict[str, str] = field(default_factory=dict)
    
    # Circuit breaker settings
    circuit_breaker_enabled: bool = True
    circuit_breaker_failure_threshold: int = 5
    circuit_breaker_recovery_timeout: float = 60.0
    
    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_messages_per_second: float = 100.0
    rate_limit_burst_size: int = 20


class CircuitBreaker:
    """Circuit breaker pattern for connection failures."""
    
    def __init__(self, failure_threshold: int, recovery_timeout: float):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "closed"  # closed, open, half-open
        
    def record_success(self):
        """Record successful operation."""
        self.failure_count = 0
        self.state = "closed"
        
    def record_failure(self):
        """Record failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"
            
    def can_attempt(self) -> bool:
        """Check if we can attempt connection."""
        if self.state == "closed":
            return True
            
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
                return True
            return False
            
        # half-open state
        return True


class RateLimiter:
    """Token bucket rate limiter."""
    
    def __init__(self, rate: float, burst_size: int):
        self.rate = rate
        self.burst_size = burst_size
        self.tokens = burst_size
        self.last_update = time.time()
        
    def can_send(self) -> bool:
        """Check if we can send a message."""
        now = time.time()
        elapsed = now - self.last_update
        
        # Add tokens based on elapsed time
        self.tokens = min(self.burst_size, self.tokens + elapsed * self.rate)
        self.last_update = now
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


class WebSocketHandler:
    """Robust WebSocket handler with advanced features."""
    
    def __init__(self, config: WebSocketConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Connection state
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.state = ConnectionState.DISCONNECTED
        self.metrics = ConnectionMetrics()
        
        # Message handling
        self.message_handlers: Dict[str, Set[Callable]] = defaultdict(set)
        self.pending_requests: Dict[str, asyncio.Future] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        
        # Control flags
        self._running = False
        self._reconnect_task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._sender_task: Optional[asyncio.Task] = None
        
        # Circuit breaker
        self.circuit_breaker = CircuitBreaker(
            config.circuit_breaker_failure_threshold,
            config.circuit_breaker_recovery_timeout
        ) if config.circuit_breaker_enabled else None
        
        # Rate limiter
        self.rate_limiter = RateLimiter(
            config.rate_limit_messages_per_second,
            config.rate_limit_burst_size
        ) if config.rate_limit_enabled else None
        
    async def connect(self) -> bool:
        """Connect to WebSocket server."""
        if self.state in (ConnectionState.CONNECTED, ConnectionState.CONNECTING):
            return True
            
        if self.circuit_breaker and not self.circuit_breaker.can_attempt():
            self.logger.warning("Circuit breaker is open, connection attempt blocked")
            return False
            
        try:
            self.state = ConnectionState.CONNECTING
            self.logger.info(f"Connecting to {self.config.url}")
            
            # Configure connection parameters
            kwargs = {
                "compression": self.config.compression,
                "max_size": self.config.max_message_size,
            }
            
            if self.config.extra_headers:
                kwargs["extra_headers"] = self.config.extra_headers
                
            # Connect
            self.websocket = await asyncio.wait_for(
                websockets.connect(self.config.url, **kwargs),
                timeout=30.0
            )
            
            self.state = ConnectionState.CONNECTED
            self.metrics.reset()
            
            if self.circuit_breaker:
                self.circuit_breaker.record_success()
                
            self.logger.info("Successfully connected")
            
            # Start background tasks
            await self._start_background_tasks()
            
            # Notify connection handlers
            await self._emit_event("connection", {"status": "connected"})
            
            return True
            
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            self.state = ConnectionState.FAILED
            
            if self.circuit_breaker:
                self.circuit_breaker.record_failure()
                
            self.metrics.errors_count += 1
            
            # Notify error handlers
            await self._emit_event("error", {"error": str(e), "type": "connection"})
            
            return False
            
    async def disconnect(self):
        """Disconnect from server."""
        self._running = False
        
        # Cancel background tasks
        tasks = []
        if self._reconnect_task:
            self._reconnect_task.cancel()
            tasks.append(self._reconnect_task)
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            tasks.append(self._heartbeat_task)
        if self._sender_task:
            self._sender_task.cancel()
            tasks.append(self._sender_task)
            
        # Wait for cancellation
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
        # Close WebSocket
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            
        self.state = ConnectionState.DISCONNECTED
        self.metrics.disconnect_time = datetime.utcnow()
        
        # Notify disconnection handlers
        await self._emit_event("connection", {"status": "disconnected"})
        
        self.logger.info("Disconnected")
        
    async def send(self, message: Dict[str, Any], timeout: Optional[float] = None) -> bool:
        """Send a message to the server."""
        if self.state != ConnectionState.CONNECTED:
            self.logger.warning("Cannot send message: not connected")
            return False
            
        # Rate limiting
        if self.rate_limiter and not self.rate_limiter.can_send():
            self.logger.warning("Rate limit exceeded, message queued")
            
        # Add to queue
        await self.message_queue.put(message)
        return True
        
    async def send_and_wait(self, message: Dict[str, Any], 
                           timeout: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """Send a message and wait for response."""
        if self.state != ConnectionState.CONNECTED:
            raise ConnectionError("Not connected")
            
        # Generate request ID if not present
        if "request_id" not in message:
            import uuid
            message["request_id"] = str(uuid.uuid4())
            
        request_id = message["request_id"]
        
        # Create future for response
        future = asyncio.Future()
        self.pending_requests[request_id] = future
        
        try:
            # Send message
            if not await self.send(message):
                raise Exception("Failed to send message")
                
            # Wait for response
            timeout = timeout or self.config.message_timeout
            response = await asyncio.wait_for(future, timeout=timeout)
            
            return response
            
        except asyncio.TimeoutError:
            self.logger.error(f"Request {request_id} timed out")
            raise
        finally:
            # Clean up
            self.pending_requests.pop(request_id, None)
            
    def on(self, event: str, handler: Callable):
        """Register an event handler."""
        self.message_handlers[event].add(handler)
        
    def off(self, event: str, handler: Callable):
        """Unregister an event handler."""
        self.message_handlers[event].discard(handler)
        
    async def _start_background_tasks(self):
        """Start background tasks."""
        self._running = True
        
        # Start heartbeat
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        
        # Start message sender
        self._sender_task = asyncio.create_task(self._sender_loop())
        
        # Start receiver
        asyncio.create_task(self._receiver_loop())
        
    async def _heartbeat_loop(self):
        """Send periodic heartbeat messages."""
        while self._running:
            try:
                await asyncio.sleep(self.config.heartbeat_interval)
                
                if self.state == ConnectionState.CONNECTED:
                    await self.websocket.ping()
                    self.logger.debug("Heartbeat sent")
                    
            except Exception as e:
                self.logger.error(f"Heartbeat error: {e}")
                
    async def _sender_loop(self):
        """Send queued messages."""
        while self._running:
            try:
                # Get message from queue
                message = await self.message_queue.get()
                
                if self.state != ConnectionState.CONNECTED:
                    # Re-queue message
                    await self.message_queue.put(message)
                    await asyncio.sleep(1)
                    continue
                    
                # Rate limiting
                if self.rate_limiter:
                    while not self.rate_limiter.can_send():
                        await asyncio.sleep(0.1)
                        
                # Send message
                data = json.dumps(message)
                await self.websocket.send(data)
                
                self.metrics.messages_sent += 1
                self.metrics.bytes_sent += len(data)
                
                self.logger.debug(f"Sent message: {message.get('type', 'unknown')}")
                
            except Exception as e:
                self.logger.error(f"Send error: {e}")
                self.metrics.errors_count += 1
                
                # Re-queue message on error
                await self.message_queue.put(message)
                
                # Trigger reconnection
                if isinstance(e, (ConnectionClosed, WebSocketException)):
                    await self._handle_disconnect()
                    
    async def _receiver_loop(self):
        """Receive messages from server."""
        while self._running:
            try:
                if self.state != ConnectionState.CONNECTED:
                    await asyncio.sleep(1)
                    continue
                    
                # Receive message
                data = await self.websocket.recv()
                self.metrics.messages_received += 1
                self.metrics.bytes_received += len(data)
                
                # Parse message
                try:
                    message = json.loads(data)
                except json.JSONDecodeError:
                    self.logger.error(f"Invalid JSON received: {data[:100]}")
                    continue
                    
                # Handle message
                await self._handle_message(message)
                
            except ConnectionClosed:
                self.logger.warning("Connection closed by server")
                await self._handle_disconnect()
                
            except Exception as e:
                self.logger.error(f"Receive error: {e}")
                self.metrics.errors_count += 1
                
                if isinstance(e, WebSocketException):
                    await self._handle_disconnect()
                    
    async def _handle_message(self, message: Dict[str, Any]):
        """Handle incoming message."""
        msg_type = message.get("type", "unknown")
        
        # Check for response to pending request
        request_id = message.get("request_id")
        if request_id and request_id in self.pending_requests:
            future = self.pending_requests[request_id]
            if not future.done():
                future.set_result(message)
                
        # Emit to handlers
        await self._emit_event(msg_type, message)
        
        # Also emit to wildcard handlers
        await self._emit_event("*", message)
        
    async def _emit_event(self, event: str, data: Any):
        """Emit event to handlers."""
        handlers = list(self.message_handlers.get(event, []))
        
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(data)
                else:
                    handler(data)
            except Exception as e:
                self.logger.error(f"Handler error for {event}: {e}")
                
    async def _handle_disconnect(self):
        """Handle disconnection."""
        if self.state == ConnectionState.DISCONNECTED:
            return
            
        self.state = ConnectionState.DISCONNECTED
        self.websocket = None
        
        # Notify handlers
        await self._emit_event("connection", {"status": "disconnected"})
        
        # Start reconnection
        if self._running and not self._reconnect_task:
            self._reconnect_task = asyncio.create_task(self._reconnect_loop())
            
    async def _reconnect_loop(self):
        """Attempt to reconnect."""
        self.state = ConnectionState.RECONNECTING
        reconnect_attempts = 0
        
        while self._running and reconnect_attempts < self.config.max_reconnect_attempts:
            reconnect_attempts += 1
            self.metrics.reconnect_attempts += 1
            
            self.logger.info(f"Reconnection attempt {reconnect_attempts}/{self.config.max_reconnect_attempts}")
            
            # Wait before reconnecting
            await asyncio.sleep(self.config.reconnect_interval)
            
            # Try to connect
            if await self.connect():
                self.logger.info("Reconnection successful")
                self._reconnect_task = None
                return
                
        self.logger.error("Max reconnection attempts reached")
        self.state = ConnectionState.FAILED
        
        # Notify failure
        await self._emit_event("connection", {"status": "failed", "reason": "max_attempts"})
        
        self._reconnect_task = None
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get connection metrics."""
        uptime = None
        if self.metrics.connect_time:
            if self.metrics.disconnect_time:
                uptime = (self.metrics.disconnect_time - self.metrics.connect_time).total_seconds()
            else:
                uptime = (datetime.utcnow() - self.metrics.connect_time).total_seconds()
                
        return {
            "state": self.state.value,
            "uptime_seconds": uptime,
            "messages_sent": self.metrics.messages_sent,
            "messages_received": self.metrics.messages_received,
            "bytes_sent": self.metrics.bytes_sent,
            "bytes_received": self.metrics.bytes_received,
            "errors_count": self.metrics.errors_count,
            "reconnect_attempts": self.metrics.reconnect_attempts,
            "circuit_breaker_state": self.circuit_breaker.state if self.circuit_breaker else None,
        }


# Example usage and integration with SemantestClient
class EnhancedSemantestClient:
    """Enhanced Semantest client using robust WebSocket handler."""
    
    def __init__(self, url: str, api_key: Optional[str] = None):
        # Configure WebSocket handler
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            
        config = WebSocketConfig(
            url=url,
            extra_headers=headers,
            heartbeat_interval=30.0,
            reconnect_interval=5.0,
            max_reconnect_attempts=10,
            rate_limit_messages_per_second=50.0
        )
        
        self.handler = WebSocketHandler(config)
        self.logger = logging.getLogger(__name__)
        
        # Register handlers
        self.handler.on("connection", self._handle_connection)
        self.handler.on("error", self._handle_error)
        
    async def connect(self) -> bool:
        """Connect to Semantest."""
        return await self.handler.connect()
        
    async def disconnect(self):
        """Disconnect from Semantest."""
        await self.handler.disconnect()
        
    async def generate_image(self, prompt: str, **kwargs) -> str:
        """Generate an image from prompt."""
        message = {
            "type": "generate_image",
            "data": {
                "prompt": prompt,
                **kwargs
            }
        }
        
        response = await self.handler.send_and_wait(message, timeout=300.0)
        return response.get("request_id")
        
    async def _handle_connection(self, data):
        """Handle connection events."""
        status = data.get("status")
        self.logger.info(f"Connection status: {status}")
        
        if status == "connected":
            # Send handshake
            await self.handler.send({
                "type": "handshake",
                "client": "metaphysical-scene-weaver",
                "version": "0.1.0"
            })
            
    async def _handle_error(self, data):
        """Handle error events."""
        self.logger.error(f"WebSocket error: {data}")
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get connection metrics."""
        return self.handler.get_metrics()