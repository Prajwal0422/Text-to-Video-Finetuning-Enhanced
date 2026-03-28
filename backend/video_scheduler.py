"""
Video Generation Scheduler
Queue and schedule video generation tasks
"""

import time
import threading
from typing import Dict, List, Optional, Callable
from queue import PriorityQueue
from datetime import datetime
from enum import Enum

class TaskPriority(Enum):
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class VideoTask:
    def __init__(self, task_id: str, prompt: str, mode: str = "fast",
                 priority: TaskPriority = TaskPriority.NORMAL):
        self.task_id = task_id
        self.prompt = prompt
        self.mode = mode
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
    
    def __lt__(self, other):
        """For priority queue comparison"""
        return self.priority.value < other.priority.value

class VideoScheduler:
    def __init__(self, max_workers: int = 2):
        self.max_workers = max_workers
        self.task_queue = PriorityQueue()
        self.tasks = {}
        self.active_tasks = {}
        self.workers = []
        self.running = False
        self.lock = threading.Lock()
        
        # Callback for task completion
        self.on_task_complete = None
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            return
        
        self.running = True
        
        # Start worker threads
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker, args=(i,), daemon=True)
            worker.start()
            self.workers.append(worker)
        
        print(f"✅ Scheduler started with {self.max_workers} workers")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5)
        
        self.workers.clear()
        print("✅ Scheduler stopped")
    
    def add_task(self, prompt: str, mode: str = "fast",
                priority: TaskPriority = TaskPriority.NORMAL) -> str:
        """Add a new task to the queue"""
        task_id = f"task_{int(time.time() * 1000)}"
        
        task = VideoTask(task_id, prompt, mode, priority)
        
        with self.lock:
            self.tasks[task_id] = task
            self.task_queue.put(task)
        
        print(f"📝 Task added: {task_id} (priority: {priority.name})")
        return task_id
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        with self.lock:
            if task_id not in self.tasks:
                return False
            
            task = self.tasks[task_id]
            
            if task.status == TaskStatus.PENDING:
                task.status = TaskStatus.CANCELLED
                print(f"❌ Task cancelled: {task_id}")
                return True
            
            return False
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """Get status of a task"""
        with self.lock:
            if task_id not in self.tasks:
                return None
            
            task = self.tasks[task_id]
            
            return {
                'task_id': task.task_id,
                'prompt': task.prompt,
                'mode': task.mode,
                'priority': task.priority.name,
                'status': task.status.value,
                'created_at': task.created_at.isoformat(),
                'started_at': task.started_at.isoformat() if task.started_at else None,
                'completed_at': task.completed_at.isoformat() if task.completed_at else None,
                'result': task.result,
                'error': task.error
            }
    
    def get_queue_stats(self) -> Dict:
        """Get queue statistics"""
        with self.lock:
            pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
            running = sum(1 for t in self.tasks.values() if t.status == TaskStatus.RUNNING)
            completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
            failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
            cancelled = sum(1 for t in self.tasks.values() if t.status == TaskStatus.CANCELLED)
            
            return {
                'total_tasks': len(self.tasks),
                'pending': pending,
                'running': running,
                'completed': completed,
                'failed': failed,
                'cancelled': cancelled,
                'queue_size': self.task_queue.qsize(),
                'active_workers': len(self.active_tasks)
            }
    
    def _worker(self, worker_id: int):
        """Worker thread that processes tasks"""
        print(f"🔧 Worker {worker_id} started")
        
        while self.running:
            try:
                # Get task from queue (with timeout)
                task = self.task_queue.get(timeout=1)
                
                # Check if cancelled
                if task.status == TaskStatus.CANCELLED:
                    continue
                
                # Process task
                self._process_task(worker_id, task)
                
            except:
                # Queue empty or timeout
                continue
        
        print(f"🔧 Worker {worker_id} stopped")
    
    def _process_task(self, worker_id: int, task: VideoTask):
        """Process a single task"""
        with self.lock:
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now()
            self.active_tasks[worker_id] = task
        
        print(f"⚙️  Worker {worker_id} processing: {task.task_id}")
        
        try:
            # Import here to avoid circular dependency
            from backend.fast_video_generator import FastVideoGenerator
            
            gen = FastVideoGenerator()
            
            # Generate video based on mode
            if task.mode == "ultra_fast":
                result = gen.generate_ultra_fast(task.prompt)
            elif task.mode == "standard":
                result = gen.generate(task.prompt)
            else:
                result = gen.generate_fast(task.prompt)
            
            # Task completed
            with self.lock:
                task.status = TaskStatus.COMPLETED
                task.completed_at = datetime.now()
                task.result = result
                del self.active_tasks[worker_id]
            
            print(f"✅ Worker {worker_id} completed: {task.task_id}")
            
            # Call completion callback
            if self.on_task_complete:
                self.on_task_complete(task)
            
        except Exception as e:
            # Task failed
            with self.lock:
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.now()
                task.error = str(e)
                del self.active_tasks[worker_id]
            
            print(f"❌ Worker {worker_id} failed: {task.task_id} - {e}")
    
    def get_pending_tasks(self) -> List[Dict]:
        """Get list of pending tasks"""
        with self.lock:
            pending = [
                self.get_task_status(t.task_id)
                for t in self.tasks.values()
                if t.status == TaskStatus.PENDING
            ]
            return sorted(pending, key=lambda x: x['created_at'])
    
    def get_completed_tasks(self, limit: int = 10) -> List[Dict]:
        """Get recent completed tasks"""
        with self.lock:
            completed = [
                self.get_task_status(t.task_id)
                for t in self.tasks.values()
                if t.status == TaskStatus.COMPLETED
            ]
            return sorted(completed, key=lambda x: x['completed_at'], reverse=True)[:limit]


# Global instance
scheduler = VideoScheduler(max_workers=2)


if __name__ == "__main__":
    print("Video Scheduler Test")
    print("=" * 60)
    
    # Start scheduler
    scheduler.start()
    
    # Add test tasks
    task1 = scheduler.add_task("ocean waves", priority=TaskPriority.HIGH)
    task2 = scheduler.add_task("mountain sunset", priority=TaskPriority.NORMAL)
    task3 = scheduler.add_task("city lights", priority=TaskPriority.LOW)
    
    # Show stats
    print("\nQueue Stats:")
    stats = scheduler.get_queue_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Wait a bit
    time.sleep(2)
    
    # Check task status
    print(f"\nTask 1 Status:")
    status = scheduler.get_task_status(task1)
    if status:
        print(f"  Status: {status['status']}")
        print(f"  Created: {status['created_at']}")
    
    # Stop scheduler
    scheduler.stop()
