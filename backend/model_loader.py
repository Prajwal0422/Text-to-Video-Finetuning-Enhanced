import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        # Using ali-vilab version which is often more accessible
        self.model_id = "ali-vilab/text-to-video-ms-1.5"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None

    def load_model(self):
        if self.pipe is not None:
            return self.pipe

        logger.info(f"Loading Text-to-Video engine: {self.model_id} on {self.device}")
        
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        
        try:
            from diffusers import TextToVideoSDPipeline
            
            # Use a very defensive loading strategy
            self.pipe = TextToVideoSDPipeline.from_pretrained(
                self.model_id, 
                torch_dtype=dtype,
                variant="fp16" if self.device == "cuda" else None
            )
            
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
            
            if self.device == "cuda":
                self.pipe.enable_model_cpu_offload()
                logger.info("GPU acceleration enabled.")
            else:
                self.pipe.to(self.device)
                logger.info("Running on CPU mode (Precision: Float32).")
                
            logger.info("Model Scope engine ready.")
            return self.pipe
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise e
