"""
Batch Processor
Process multiple video generation requests in queue
"""

import time
import threading
from typing import List, Dict, Optional, Callable
from queue import Queue, Empty
from dataclasses import dataclass
from datetime import datetime

@dataclass
class BatchJob:
    """Represents a batch video generation job"""
    id: str
    prompt: str
    status: str = 'pending'  # pending, processing, completed, failed
    created_at: float = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()

class BatchProcessor:
    """Processes video generation jobs in batches"""
    
    def __init__(self, max_workers: int = 2):
        self.max_workers = max_workers
        self.job_queue = Queue()
        self.jobs: Dict[str, BatchJob] = {}
        self.workers: List[threading.Thread] = []
        self.running = False
        self.lock = threading.Lock()
    
    def add_job(self, prompt: str) -> str:
        """
        Add a job to the queue
        
        Args:
            prompt: Video generation prompt
        
        Returns:
            Job ID
        """
        job_id = f"job_{int(time.time() * 1000)}"
        job = BatchJob(id=job_id, prompt=prompt)
        
        with self.lock:
            self.jobs[job_id] = job
            self.job_queue.put(job_id)
        
        return job_id
    
    def add_multiple_jobs(self, prompts: List[str]) -> List[str]:
        """Add multiple jobs at once"""
        job_ids = []
        for prompt in prompts:
            job_id = self.add_job(prompt)
            job_ids.append(job_id)
        return job_ids
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Get status of a specific job"""
        with self.lock:
            job = self.jobs.get(job_id)
            if not job:
                return None
            
            return {
                'id': job.id,
                'prompt': job.prompt,
                'status': job.status,
                'created_at': datetime.fromtimestamp(job.created_at).isoformat(),
                'started_at': datetime.fromtimestamp(job.started_at).isoformat() if job.started_at else None,
                'completed_at': datetime.fromtimestamp(job.completed_at).isoformat() if job.completed_at else None,
                'result': job.result,
                'error': job.error
            }
    
    def get_all_jobs(self) -> List[Dict]:
        """Get status of all jobs"""
        with self.lock:
            return [self.get_job_status(job_id) for job_id in self.jobs.keys()]
    
    def get_queue_stats(self) -> Dict:
        """Get queue statistics"""
        with self.lock:
            pending = sum(1 for job in self.jobs.values() if job.status == 'pending')
            processing = sum(1 for job in self.jobs.values() if job.status == 'processing')
            completed = sum(1 for job in self.jobs.values() if job.status == 'completed')
            failed = sum(1 for job in self.jobs.values() if job.status == 'failed')
            
            return {
                'total_jobs': len(self.jobs),
                'pending': pending,
                'processing': processing,
                'completed': completed,
                'failed': failed,
                'queue_size': self.job_queue.qsize(),
                'workers': len(self.workers),
                'running': self.running
            }
    
    def _worker(self, worker_id: int, process_func: Callable):
        """Worker thread that processes jobs"""
        print(f"Worker {worker_id} started")
        
        while self.running:
            try:
                # Get job from queue (timeout to check running flag)
                job_id = self.job_queue.get(timeout=1)
                
                with self.lock:
                    job = self.jobs.get(job_id)
                    if not job:
                        continue
                    
                    job.status = 'processing'
                    job.started_at = time.time()
                
                print(f"Worker {worker_id} processing job {job_id}: '{job.prompt}'")
                
                # Process the job
                try:
                    result = process_func(job.prompt)
                    
                    with self.lock:
                        job.status = 'completed'
                        job.completed_at = time.time()
                        job.result = result
                    
                    print(f"Worker {worker_id} completed job {job_id}")
                
                except Exception as e:
                    with self.lock:
                        job.status = 'failed'
                        job.completed_at = time.time()
                        job.error = str(e)
                    
                    print(f"Worker {worker_id} failed job {job_id}: {e}")
                
                finally:
                    self.job_queue.task_done()
            
            except Empty:
                # No jobs in queue, continue
                continue
            except Exception as e:
                print(f"Worker {worker_id} error: {e}")
        
        print(f"Worker {worker_id} stopped")
    
    def start(self, process_func: Callable):
        """
        Start the batch processor
        
        Args:
            process_func: Function to process each job (takes prompt, returns result)
        """
        if self.running:
            print("Batch processor already running")
            return
        
        self.running = True
        
        # Start worker threads
        for i in range(self.max_workers):
            worker = threading.Thread(
                target=self._worker,
                args=(i + 1, process_func),
                daemon=True
            )
            worker.start()
            self.workers.append(worker)
        
        print(f"Batch processor started with {self.max_workers} workers")
    
    def stop(self):
        """Stop the batch processor"""
        if not self.running:
            return
        
        print("Stopping batch processor...")
        self.running = False
        
        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5)
        
        self.workers.clear()
        print("Batch processor stopped")
    
    def wait_for_completion(self, timeout: Optional[float] = None):
        """Wait for all jobs to complete"""
        self.job_queue.join()
        
        # Wait for all jobs to be completed or failed
        start_time = time.time()
        while True:
            with self.lock:
                pending = sum(1 for job in self.jobs.values() if job.status in ['pending', 'processing'])
                if pending == 0:
                    break
            
            if timeout and (time.time() - start_time) > timeout:
                print("Timeout waiting for jobs to complete")
                break
            
            time.sleep(0.5)


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("BATCH PROCESSOR - TEST")
    print("=" * 60)
    
    # Mock processing function
    def mock_process(prompt: str) -> Dict:
        """Mock video generation"""
        print(f"  Processing: '{prompt}'")
        time.sleep(2)  # Simulate processing
        return {
            'success': True,
            'video_path': f'/outputs/video_{prompt[:10]}.mp4',
            'duration': 2.0
        }
    
    # Create processor
    processor = BatchProcessor(max_workers=2)
    
    # Add jobs
    prompts = [
        "ocean waves",
        "mountain sunset",
        "city lights",
        "forest path"
    ]
    
    print(f"\nAdding {len(prompts)} jobs...")
    job_ids = processor.add_multiple_jobs(prompts)
    
    for job_id in job_ids:
        print(f"  Added: {job_id}")
    
    # Start processing
    print("\nStarting batch processor...")
    processor.start(mock_process)
    
    # Monitor progress
    print("\nMonitoring progress...")
    while True:
        stats = processor.get_queue_stats()
        print(f"  Pending: {stats['pending']}, Processing: {stats['processing']}, Completed: {stats['completed']}, Failed: {stats['failed']}")
        
        if stats['pending'] == 0 and stats['processing'] == 0:
            break
        
        time.sleep(1)
    
    # Stop processor
    processor.stop()
    
    # Show results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    
    for job_id in job_ids:
        status = processor.get_job_status(job_id)
        print(f"\nJob: {job_id}")
        print(f"  Prompt: {status['prompt']}")
        print(f"  Status: {status['status']}")
        if status['result']:
            print(f"  Result: {status['result']}")
