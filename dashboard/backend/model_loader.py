import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelLoader:
    """
    Singleton Model Loader for handling GPU-accelerated video diffusion models.
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.model_id = "cerspense/zeroscope_v2_576w"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = None

    def load_model(self):
        if self.pipe is not None:
            return self.pipe

        logger.info(f"Loading Text-to-Video engine: {self.model_id} on {self.device}")
        
        dtype = torch.float16 if self.device == "cuda" else torch.float32
        
        try:
            # More robust loading: let diffusers handle safetensors detection
            # and only use fp16 if we are on CUDA
            load_args = {
                "torch_dtype": dtype,
            }
            if self.device == "cuda":
                load_args["variant"] = "fp16"
                load_args["use_safetensors"] = True
            
            self.pipe = DiffusionPipeline.from_pretrained(
                self.model_id, 
                **load_args
            )
            self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
            
            if self.device == "cuda":
                self.pipe.enable_model_cpu_offload()
                logger.info("GPU acceleration with FP16 and CPU Offload enabled.")
            else:
                self.pipe.to(self.device)
                
            logger.info("Model Scope engine ready for inference.")
            return self.pipe
        except Exception as e:
            logger.error(f"Critical failure loading model: {e}")
            raise e
