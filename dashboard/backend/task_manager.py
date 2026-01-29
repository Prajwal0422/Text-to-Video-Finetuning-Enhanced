import asyncio
import concurrent.futures
from typing import Dict, Any, Callable
from backend.inference import generate_video_async

class TaskManager:
    def __init__(self):
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

    async def run_generation(self, task_id: str, prompt: str, params: Dict[str, Any], callback: Callable):
        main_loop = asyncio.get_running_loop()
        try:
            # Offload the heavy torch inference to a thread to avoid blocking the main loop
            video_url = await main_loop.run_in_executor(
                self.executor,
                lambda: asyncio.run(generate_video_async(
                    prompt=prompt,
                    num_frames=params.get("num_frames", 24),
                    num_steps=params.get("num_steps", 25),
                    status_callback=callback,
                    main_loop=main_loop # Pass the main loop for callbacks
                ))
            )
            return video_url
        except Exception as e:
            raise e

task_manager = TaskManager()
