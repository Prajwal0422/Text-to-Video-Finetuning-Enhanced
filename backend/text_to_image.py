import torch
from diffusers import StableDiffusionPipeline
import logging

logger = logging.getLogger(__name__)

class T2IEngine:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # Stable Diffusion v1.5 is the most reliable fallback for older diffusers versions
        self.model_id = "runwayml/stable-diffusion-v1-5"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None

    def load(self):
        if self.pipe: return self.pipe
        
        logger.info(f"Loading Stable T2I Engine: {self.model_id} on {self.device}")
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        
        try:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id, 
                torch_dtype=dtype,
                safety_checker=None # Speed up and reduce memory
            )
            self.pipe.to(self.device)
            logger.info("T2I Engine Ready.")
            return self.pipe
        except Exception as e:
            logger.error(f"T2I Load Failure: {e}")
            raise e

    def generate(self, prompt, num_steps=10, seed=None):
        pipe = self.load()
        generator = torch.Generator(device=self.device).manual_seed(seed) if seed else None
        
        # Fast mode: 10 steps. HQ mode: 25 steps.
        image = pipe(
            prompt=prompt, 
            num_inference_steps=num_steps, 
            generator=generator
        ).images[0]
        
        return image
