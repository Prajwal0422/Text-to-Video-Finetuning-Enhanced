import torch
from diffusers import AutoPipelineForText2Image
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
        # SD-Turbo is the fastest high-quality model (1-step generation)
        self.model_id = "stabilityai/sd-turbo"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None

    def load(self):
        if self.pipe: return self.pipe
        
        logger.info(f"Loading Hyper-Fast T2I Engine: {self.model_id} on {self.device}")
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        
        try:
            self.pipe = AutoPipelineForText2Image.from_pretrained(
                self.model_id, 
                torch_dtype=dtype, 
                variant="fp16" if self.device == "cuda" else None
            )
            self.pipe.to(self.device)
            logger.info("T2I Engine Ready.")
            return self.pipe
        except Exception as e:
            logger.error(f"T2I Load Failure: {e}")
            raise e

    def generate(self, prompt, num_steps=1, seed=None):
        pipe = self.load()
        generator = torch.Generator(device=self.device).manual_seed(seed) if seed else None
        
        # SD-Turbo generates high quality in 1-4 steps
        image = pipe(
            prompt=prompt, 
            num_inference_steps=num_steps, 
            guidance_scale=0.0,
            generator=generator
        ).images[0]
        
        return image
