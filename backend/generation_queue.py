"""
Generation Queue System - Task Queue with Progress Updates
Manages video generation requests sequentially with WebSocket updates
"""

import asyncio
import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Task status states"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class GenerationTask:
    """Represents a video generation task"""
    task_id: str
    prompt: str
    status: TaskStatus = TaskStatus.QUEUED
    progress: int = 0
    message: str = "Queued"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary"""
        return {
            'task_id': self.task_id,
            'prompt': self.prompt,
            'status': self.status.value,
            'progress': self.progress,
            'message': self.message,
            'result': self.result,
            'error': self.error,
            'created_at': self.created_at.isoformat(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class GenerationQueue:
    """
    Task queue for video generation
    
    Features:
    - Sequential processing (one at a time)
    - Progress tracking per task
    - WebSocket updates
    - Task history
    - Queue statistics
    """
    
    def __init__(self, max_history: int = 100):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.tasks: Dict[str, GenerationTask] = {}
        self.current_task: Optional[GenerationTask] = None
        self.max_history = max_history
        self.is_processing = False
        self.progress_callbacks: Dict[str, Callable] = {}
    
    def create_task(self, prompt: str) -> str:
        """
        Create new generation task
        
        Args:
            prompt: Video generation prompt
        
        Returns:
            task_id: Unique task identifier
        """
        task_id = str(uuid.uuid4())
        task = GenerationTask(
            task_id=task_id,
            prompt=prompt
        )
        
        self.tasks[task_id] = task
        logger.info(f"📝 Task created: {task_id[:8]}... - '{prompt[:50]}'")
        
        return task_id
    
    async def enqueue(self, prompt: str) -> str:
        """
        Add task to queue
        
        Args:
            prompt: Video generation prompt
        
        Returns:
            task_id: Unique task identifier
        """
        task_id = self.create_task(prompt)
        task = self.tasks[task_id]
        
        await self.queue.put(task)
        
        queue_size = self.queue.qsize()
        logger.info(f"➕ Task queued: {task_id[:8]}... (Queue size: {queue_size})")
        
        # Update task message
        task.message = f"Queued (position: {queue_size})"
        await self._notify_progress(task)
        
        return task_id
    
    def register_progress_callback(self, task_id: str, callback: Callable):
        """Register callback for task progress updates"""
        self.progress_callbacks[task_id] = callback
        logger.info(f"📡 Progress callback registered for {task_id[:8]}...")
    
    def unregister_progress_callback(self, task_id: str):
        """Unregister progress callback"""
        if task_id in self.progress_callbacks:
            del self.progress_callbacks[task_id]
    
    async def _notify_progress(self, task: GenerationTask):
        """Send progress update via callback"""
        if task.task_id in self.progress_callbacks:
            callback = self.progress_callbacks[task.task_id]
            try:
                await callback(task.to_dict())
            except Exception as e:
                logger.error(f"❌ Progress callback error: {e}")
    
    async def update_task_progress(
        self,
        task_id: str,
        progress: int,
        message: str
    ):
        """
        Update task progress
        
        Args:
            task_id: Task identifier
            progress: Progress percentage (0-100)
            message: Status message
        """
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        task.progress = progress
        task.message = message
        
        logger.info(f"📊 {task_id[:8]}... - {progress}% - {message}")
        
        await self._notify_progress(task)
    
    async def process_queue(self, generator_func: Callable):
        """
        Process tasks from queue sequentially
        
        Args:
            generator_func: Async function(task) -> result
        """
        if self.is_processing:
            logger.warning("⚠️  Queue already processing")
            return
        
        self.is_processing = True
        logger.info("🚀 Queue processor started")
        
        try:
            while True:
                # Get next task (wait if queue empty)
                task = await self.queue.get()
                self.current_task = task
                
                logger.info(f"▶️  Processing: {task.task_id[:8]}... - '{task.prompt[:50]}'")
                
                # Update status
                task.status = TaskStatus.PROCESSING
                task.started_at = datetime.now()
                task.progress = 0
                task.message = "Starting generation..."
                await self._notify_progress(task)
                
                try:
                    # Execute generation
                    result = await generator_func(task)
                    
                    # Mark as completed
                    task.status = TaskStatus.COMPLETED
                    task.completed_at = datetime.now()
                    task.progress = 100
                    task.message = "Generation complete!"
                    task.result = result
                    
                    logger.info(f"✅ Completed: {task.task_id[:8]}...")
                    
                except Exception as e:
                    # Mark as failed
                    task.status = TaskStatus.FAILED
                    task.completed_at = datetime.now()
                    task.error = str(e)
                    task.message = f"Failed: {str(e)[:100]}"
                    
                    logger.error(f"❌ Failed: {task.task_id[:8]}... - {e}")
                
                finally:
                    await self._notify_progress(task)
                    self.current_task = None
                    self.queue.task_done()
                    
                    # Cleanup old tasks
                    self._cleanup_history()
        
        finally:
            self.is_processing = False
            logger.info("🛑 Queue processor stopped")
    
    def _cleanup_history(self):
        """Remove old completed tasks to limit memory"""
        completed_tasks = [
            (task_id, task) for task_id, task in self.tasks.items()
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]
        ]
        
        if len(completed_tasks) > self.max_history:
            # Sort by completion time
            completed_tasks.sort(key=lambda x: x[1].completed_at or datetime.now())
            
            # Remove oldest
            to_remove = len(completed_tasks) - self.max_history
            for task_id, _ in completed_tasks[:to_remove]:
                del self.tasks[task_id]
                logger.info(f"🗑️  Removed old task: {task_id[:8]}...")
    
    def get_task(self, task_id: str) -> Optional[GenerationTask]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get queue statistics"""
        queued = sum(1 for t in self.tasks.values() if t.status == TaskStatus.QUEUED)
        processing = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PROCESSING)
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        
        return {
            'is_processing': self.is_processing,
            'queue_size': self.queue.qsize(),
            'current_task': self.current_task.to_dict() if self.current_task else None,
            'stats': {
                'queued': queued,
                'processing': processing,
                'completed': completed,
                'failed': failed,
                'total': len(self.tasks)
            }
        }
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel queued task
        
        Args:
            task_id: Task to cancel
        
        Returns:
            True if cancelled, False if not found or already processing
        """
        task = self.get_task(task_id)
        
        if not task:
            return False
        
        if task.status != TaskStatus.QUEUED:
            logger.warning(f"⚠️  Cannot cancel task {task_id[:8]}... (status: {task.status.value})")
            return False
        
        task.status = TaskStatus.CANCELLED
        task.message = "Cancelled by user"
        logger.info(f"🚫 Task cancelled: {task_id[:8]}...")
        
        return True


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("GENERATION QUEUE SYSTEM - TEST")
    print("=" * 60)
    
    async def mock_generator(task: GenerationTask) -> Dict[str, Any]:
        """Mock video generator"""
        # Simulate generation stages
        stages = [
            (20, "Analyzing prompt..."),
            (40, "Fetching clips..."),
            (60, "Composing video..."),
            (80, "Rendering..."),
            (100, "Complete!")
        ]
        
        queue = GenerationQueue()
        
        for progress, message in stages:
            await queue.update_task_progress(task.task_id, progress, message)
            await asyncio.sleep(1)
        
        return {
            'video_path': f'/outputs/video_{task.task_id[:8]}.mp4',
            'duration': 5.0
        }
    
    async def test_queue():
        queue = GenerationQueue()
        
        # Add tasks
        task1 = await queue.enqueue("A beautiful sunset")
        task2 = await queue.enqueue("Ocean waves")
        task3 = await queue.enqueue("City lights")
        
        print(f"\n📊 Queue status:")
        print(queue.get_queue_status())
        
        # Process queue
        await queue.process_queue(mock_generator)
        
        print(f"\n✅ Final status:")
        print(queue.get_queue_status())
    
    asyncio.run(test_queue())
