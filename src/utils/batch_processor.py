"""Batch processing optimizations for handling multiple scenes efficiently."""

import asyncio
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from collections import defaultdict
import time
import logging
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json


@dataclass
class BatchConfig:
    """Configuration for batch processing."""
    max_batch_size: int = 100
    max_concurrent_workers: int = 4
    timeout_per_item: float = 30.0
    enable_caching: bool = True
    cache_ttl: int = 3600  # 1 hour
    enable_deduplication: bool = True
    priority_queue: bool = True


@dataclass 
class BatchItem:
    """Individual item in a batch."""
    id: str
    data: Dict[str, Any]
    priority: int = 0
    callback: Optional[Callable] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def get_hash(self) -> str:
        """Get hash for deduplication."""
        return hashlib.md5(
            json.dumps(self.data, sort_keys=True).encode()
        ).hexdigest()


@dataclass
class BatchResult:
    """Result of batch processing."""
    successful: List[Dict[str, Any]]
    failed: List[Dict[str, Any]]
    cached: List[Dict[str, Any]]
    total_time: float
    items_per_second: float


class BatchProcessor:
    """Optimized batch processor for scene generation."""
    
    def __init__(self, config: Optional[BatchConfig] = None):
        self.config = config or BatchConfig()
        self.logger = logging.getLogger(__name__)
        
        # Processing queues
        self.pending_queue = asyncio.PriorityQueue() if self.config.priority_queue else asyncio.Queue()
        self.processing = {}
        
        # Caching
        self.cache = {} if self.config.enable_caching else None
        self.cache_hits = 0
        self.cache_misses = 0
        
        # Deduplication
        self.seen_hashes = set() if self.config.enable_deduplication else None
        
        # Worker management
        self.workers = []
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_workers)
        self._running = False
        
        # Metrics
        self.metrics = {
            "total_processed": 0,
            "total_failed": 0,
            "total_cached": 0,
            "average_processing_time": 0.0
        }
    
    async def add_batch(self, items: List[BatchItem]) -> str:
        """Add a batch of items for processing."""
        batch_id = f"batch_{int(time.time())}_{len(items)}"
        
        added_count = 0
        for item in items:
            # Check deduplication
            if self.config.enable_deduplication:
                item_hash = item.get_hash()
                if item_hash in self.seen_hashes:
                    self.logger.debug(f"Skipping duplicate item: {item.id}")
                    continue
                self.seen_hashes.add(item_hash)
            
            # Add to queue
            if self.config.priority_queue:
                await self.pending_queue.put((-item.priority, item))
            else:
                await self.pending_queue.put(item)
            
            added_count += 1
        
        self.logger.info(f"Added batch {batch_id} with {added_count}/{len(items)} items")
        return batch_id
    
    async def process_batch(self, items: List[BatchItem], 
                           processor_func: Callable) -> BatchResult:
        """Process a batch of items with optimizations."""
        start_time = time.time()
        
        # Results tracking
        successful = []
        failed = []
        cached = []
        
        # Check cache first
        items_to_process = []
        if self.config.enable_caching:
            for item in items:
                cache_key = self._get_cache_key(item)
                if cache_key in self.cache:
                    cached_result, cached_time = self.cache[cache_key]
                    if time.time() - cached_time < self.config.cache_ttl:
                        cached.append({
                            "id": item.id,
                            "result": cached_result,
                            "cached": True
                        })
                        self.cache_hits += 1
                        continue
                
                items_to_process.append(item)
                self.cache_misses += 1
        else:
            items_to_process = items
        
        # Process items concurrently
        if items_to_process:
            # Create tasks for concurrent processing
            tasks = []
            for item in items_to_process:
                task = asyncio.create_task(
                    self._process_single_item(item, processor_func)
                )
                tasks.append((item, task))
            
            # Wait for all tasks with timeout
            for item, task in tasks:
                try:
                    result = await asyncio.wait_for(
                        task, 
                        timeout=self.config.timeout_per_item
                    )
                    
                    successful.append({
                        "id": item.id,
                        "result": result,
                        "cached": False
                    })
                    
                    # Update cache
                    if self.config.enable_caching:
                        cache_key = self._get_cache_key(item)
                        self.cache[cache_key] = (result, time.time())
                    
                    # Call callback if provided
                    if item.callback:
                        await self._call_callback(item.callback, result)
                    
                except asyncio.TimeoutError:
                    failed.append({
                        "id": item.id,
                        "error": "Processing timeout",
                        "data": item.data
                    })
                    self.metrics["total_failed"] += 1
                    
                except Exception as e:
                    failed.append({
                        "id": item.id,
                        "error": str(e),
                        "data": item.data
                    })
                    self.metrics["total_failed"] += 1
        
        # Calculate metrics
        total_time = time.time() - start_time
        total_items = len(successful) + len(failed) + len(cached)
        items_per_second = total_items / total_time if total_time > 0 else 0
        
        # Update global metrics
        self.metrics["total_processed"] += len(successful)
        self.metrics["total_cached"] += len(cached)
        
        return BatchResult(
            successful=successful,
            failed=failed,
            cached=cached,
            total_time=total_time,
            items_per_second=items_per_second
        )
    
    async def _process_single_item(self, item: BatchItem, 
                                  processor_func: Callable) -> Any:
        """Process a single item."""
        # Track processing
        self.processing[item.id] = {
            "start_time": time.time(),
            "item": item
        }
        
        try:
            # Run processor function
            if asyncio.iscoroutinefunction(processor_func):
                result = await processor_func(item.data)
            else:
                # Run sync function in executor
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    self.executor, 
                    processor_func, 
                    item.data
                )
            
            return result
            
        finally:
            # Clean up tracking
            if item.id in self.processing:
                del self.processing[item.id]
    
    async def start_workers(self, processor_func: Callable):
        """Start background workers for continuous processing."""
        self._running = True
        
        # Start worker tasks
        for i in range(self.config.max_concurrent_workers):
            worker = asyncio.create_task(
                self._worker_loop(i, processor_func)
            )
            self.workers.append(worker)
        
        self.logger.info(f"Started {self.config.max_concurrent_workers} workers")
    
    async def stop_workers(self):
        """Stop all workers gracefully."""
        self._running = False
        
        # Cancel all workers
        for worker in self.workers:
            worker.cancel()
        
        # Wait for cancellation
        await asyncio.gather(*self.workers, return_exceptions=True)
        
        self.workers.clear()
        self.logger.info("All workers stopped")
    
    async def _worker_loop(self, worker_id: int, processor_func: Callable):
        """Worker loop for processing items from queue."""
        self.logger.info(f"Worker {worker_id} started")
        
        while self._running:
            try:
                # Get item from queue
                if self.config.priority_queue:
                    priority, item = await self.pending_queue.get()
                else:
                    item = await self.pending_queue.get()
                
                # Process item
                try:
                    result = await self._process_single_item(item, processor_func)
                    
                    # Handle success
                    if item.callback:
                        await self._call_callback(item.callback, result)
                    
                except Exception as e:
                    self.logger.error(f"Worker {worker_id} error processing {item.id}: {e}")
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Worker {worker_id} unexpected error: {e}")
                await asyncio.sleep(1)
        
        self.logger.info(f"Worker {worker_id} stopped")
    
    def _get_cache_key(self, item: BatchItem) -> str:
        """Generate cache key for an item."""
        return f"cache_{item.get_hash()}"
    
    async def _call_callback(self, callback: Callable, result: Any):
        """Call callback function safely."""
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(result)
            else:
                callback(result)
        except Exception as e:
            self.logger.error(f"Callback error: {e}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get processing metrics."""
        cache_hit_rate = 0.0
        if self.cache_hits + self.cache_misses > 0:
            cache_hit_rate = self.cache_hits / (self.cache_hits + self.cache_misses)
        
        return {
            **self.metrics,
            "queue_size": self.pending_queue.qsize(),
            "processing_count": len(self.processing),
            "cache_size": len(self.cache) if self.cache else 0,
            "cache_hit_rate": cache_hit_rate,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses
        }
    
    async def wait_for_completion(self, timeout: Optional[float] = None):
        """Wait for all queued items to be processed."""
        start_time = time.time()
        
        while self.pending_queue.qsize() > 0 or len(self.processing) > 0:
            if timeout and (time.time() - start_time) > timeout:
                raise asyncio.TimeoutError("Batch processing timeout")
            
            await asyncio.sleep(0.1)
    
    def clear_cache(self):
        """Clear the processing cache."""
        if self.cache:
            self.cache.clear()
            self.cache_hits = 0
            self.cache_misses = 0
            self.logger.info("Cache cleared")


# Specialized batch processor for scene generation
class SceneBatchProcessor(BatchProcessor):
    """Batch processor optimized for scene generation."""
    
    def __init__(self, scene_weaver, config: Optional[BatchConfig] = None):
        super().__init__(config)
        self.scene_weaver = scene_weaver
        
        # Scene-specific optimizations
        self.character_cache = {}
        self.context_cache = defaultdict(list)
    
    async def process_script_batch(self, script_entries: List[Dict[str, Any]]) -> BatchResult:
        """Process a batch of script entries with scene-specific optimizations."""
        
        # Pre-process for better context awareness
        self._build_context_cache(script_entries)
        
        # Convert to BatchItems with priority based on narrative position
        items = []
        for i, entry in enumerate(script_entries):
            # Earlier scenes have higher priority
            priority = len(script_entries) - i
            
            item = BatchItem(
                id=entry.get("id", f"scene_{i}"),
                data=entry,
                priority=priority,
                metadata={
                    "position": i,
                    "total": len(script_entries)
                }
            )
            items.append(item)
        
        # Process with scene processor
        return await self.process_batch(items, self._process_scene_entry)
    
    async def _process_scene_entry(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single scene entry."""
        # Use scene weaver to process
        from ..core.script_parser import ScriptEntry
        
        entry = ScriptEntry(
            id=entry_data.get("id"),
            speaker=entry_data.get("speaker"),
            dialogue=entry_data.get("dialogue"),
            panel_count=entry_data.get("panel_count"),
            stage_directions=entry_data.get("stage_directions", []),
            metadata=entry_data.get("metadata", [])
        )
        
        # Get context from cache
        position = entry_data.get("position", 0)
        context = self.context_cache.get(position, [])
        
        # Process with scene weaver
        enriched_scene = self.scene_weaver.process_entry(
            entry, 
            position, 
            context
        )
        
        return {
            "prompt": enriched_scene.prompt,
            "metadata": enriched_scene.metadata,
            "philosophy": enriched_scene.philosophy,
            "emotion": enriched_scene.emotion
        }
    
    def _build_context_cache(self, entries: List[Dict[str, Any]]):
        """Build context cache for efficient processing."""
        # Create context windows for each entry
        window_size = 3  # Consider 3 entries before and after
        
        for i, entry in enumerate(entries):
            # Get surrounding entries
            start = max(0, i - window_size)
            end = min(len(entries), i + window_size + 1)
            
            context = entries[start:end]
            self.context_cache[i] = context
    
    async def optimize_for_semantest(self, entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize batch for Semantest processing."""
        optimized = []
        
        for entry in entries:
            # Group by visual similarity
            visual_hash = self._get_visual_hash(entry)
            
            # Reuse similar visual settings
            if visual_hash in self.cache:
                cached_visual = self.cache[visual_hash]
                entry["visual_base"] = cached_visual
            
            optimized.append(entry)
        
        return optimized
    
    def _get_visual_hash(self, entry: Dict[str, Any]) -> str:
        """Generate hash based on visual elements."""
        visual_elements = {
            "location": entry.get("location", "unknown"),
            "time": entry.get("time_of_day", "day"),
            "mood": entry.get("mood", "neutral")
        }
        
        return hashlib.md5(
            json.dumps(visual_elements, sort_keys=True).encode()
        ).hexdigest()