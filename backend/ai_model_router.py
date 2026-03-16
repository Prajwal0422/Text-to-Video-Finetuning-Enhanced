"""
AI Model Router - Multi-Model Fallback System
Routes requests through primary → fallback → emergency models
"""

import logging
from typing import Dict, Any, Optional, Callable
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Available model types"""
    PRIMARY = "primary"
    FALLBACK = "fallback"
    EMERGENCY = "emergency"


class ModelConfig:
    """Model configuration"""
    def __init__(self, name: str, endpoint: str, timeout: int = 60):
        self.name = name
        self.endpoint = endpoint
        self.timeout = timeout
        self.is_available = True
        self.failure_count = 0
        self.max_failures = 3


class ModelRouter:
    """
    Routes AI generation requests through multiple models
    
    Strategy:
    1. Try primary model (best quality)
    2. If busy/failed → try fallback model (good quality)
    3. If busy/failed → try emergency model (basic quality)
    """
    
    def __init__(self):
        # Configure models
        self.models = {
            ModelType.PRIMARY: ModelConfig(
                name="pexels_api",
                endpoint="https://api.pexels.com/videos",
                timeout=60
            ),
            ModelType.FALLBACK: ModelConfig(
                name="pixabay_api",
                endpoint="https://pixabay.com/api/videos",
                timeout=45
            ),
            ModelType.EMERGENCY: ModelConfig(
                name="local_cache",
                endpoint="local",
                timeout=30
            )
        }
        
        self.current_model = None
        self.routing_history = []
    
    def get_available_model(self) -> Optional[ModelConfig]:
        """
        Get next available model in priority order
        
        Returns:
            ModelConfig or None if all models unavailable
        """
        priority_order = [
            ModelType.PRIMARY,
            ModelType.FALLBACK,
            ModelType.EMERGENCY
        ]
        
        for model_type in priority_order:
            model = self.models[model_type]
            
            if model.is_available and model.failure_count < model.max_failures:
                logger.info(f"🎯 Selected model: {model.name}")
                self.current_model = model_type
                return model
        
        logger.error("💥 All models unavailable!")
        return None
    
    def mark_model_failed(self, model_type: ModelType, error: Exception):
        """Mark model as failed and increment failure count"""
        model = self.models[model_type]
        model.failure_count += 1
        
        logger.warning(
            f"❌ {model.name} failed "
            f"({model.failure_count}/{model.max_failures}): {str(error)[:100]}"
        )
        
        if model.failure_count >= model.max_failures:
            model.is_available = False
            logger.error(f"🚫 {model.name} marked as unavailable")
    
    def mark_model_success(self, model_type: ModelType):
        """Reset failure count on success"""
        model = self.models[model_type]
        if model.failure_count > 0:
            logger.info(f"✅ {model.name} recovered")
        model.failure_count = 0
        model.is_available = True
    
    def route_request(
        self,
        request_func: Callable,
        *args,
        on_model_switch: Optional[Callable[[str, str], None]] = None,
        **kwargs
    ) -> Any:
        """
        Route request through available models
        
        Args:
            request_func: Function to execute (model_config, *args, **kwargs)
            *args: Function arguments
            on_model_switch: Callback(from_model, to_model)
            **kwargs: Function keyword arguments
        
        Returns:
            Result from successful model
        
        Raises:
            Exception if all models fail
        """
        last_exception = None
        attempted_models = []
        
        while True:
            # Get next available model
            model_config = self.get_available_model()
            
            if not model_config:
                # All models exhausted
                logger.error(
                    f"💥 All models failed. Attempted: {attempted_models}"
                )
                raise Exception(
                    f"All models unavailable. "
                    f"Tried: {', '.join(attempted_models)}"
                )
            
            model_type = self.current_model
            attempted_models.append(model_config.name)
            
            # Notify about model switch
            if len(attempted_models) > 1 and on_model_switch:
                on_model_switch(attempted_models[-2], model_config.name)
            
            try:
                logger.info(
                    f"🔄 Attempting with {model_config.name} "
                    f"(timeout: {model_config.timeout}s)"
                )
                
                # Execute request with model config
                result = request_func(model_config, *args, **kwargs)
                
                # Success!
                self.mark_model_success(model_type)
                self.routing_history.append({
                    'model': model_config.name,
                    'status': 'success',
                    'attempts': len(attempted_models)
                })
                
                logger.info(
                    f"✅ Success with {model_config.name} "
                    f"(attempt {len(attempted_models)})"
                )
                
                return result
                
            except Exception as e:
                last_exception = e
                
                # Mark model as failed
                self.mark_model_failed(model_type, e)
                self.routing_history.append({
                    'model': model_config.name,
                    'status': 'failed',
                    'error': str(e)[:100]
                })
                
                # Check if we should try next model
                error_str = str(e).lower()
                retryable_errors = [
                    'busy', 'traffic', 'timeout', 'unavailable',
                    'rate limit', '503', '429'
                ]
                
                is_retryable = any(err in error_str for err in retryable_errors)
                
                if not is_retryable:
                    logger.error(f"💥 Non-retryable error: {str(e)[:100]}")
                    raise
                
                logger.warning(
                    f"⚠️  {model_config.name} failed, trying next model..."
                )
                # Continue to next model
    
    def get_stats(self) -> Dict[str, Any]:
        """Get routing statistics"""
        return {
            'models': {
                model_type.value: {
                    'name': config.name,
                    'available': config.is_available,
                    'failures': config.failure_count
                }
                for model_type, config in self.models.items()
            },
            'current_model': self.current_model.value if self.current_model else None,
            'routing_history': self.routing_history[-10:]  # Last 10 routes
        }
    
    def reset_models(self):
        """Reset all models to available state"""
        for model in self.models.values():
            model.is_available = True
            model.failure_count = 0
        logger.info("🔄 All models reset to available")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("AI MODEL ROUTER - TEST")
    print("=" * 60)
    
    router = ModelRouter()
    
    # Simulate request function
    attempt = 0
    
    def generate_video(model_config: ModelConfig, prompt: str) -> str:
        global attempt
        attempt += 1
        
        # Simulate primary and fallback failing
        if model_config.name == "pexels_api" and attempt <= 1:
            raise Exception("Model experiencing high traffic")
        
        if model_config.name == "pixabay_api" and attempt <= 2:
            raise Exception("Service temporarily unavailable")
        
        # Emergency succeeds
        return f"Generated with {model_config.name}: {prompt}"
    
    # Test routing
    try:
        result = router.route_request(
            generate_video,
            "A beautiful sunset",
            on_model_switch=lambda f, t: print(f"🔀 Switching: {f} → {t}")
        )
        print(f"\n✅ Result: {result}")
        print(f"\n📊 Stats:\n{router.get_stats()}")
    except Exception as e:
        print(f"\n❌ Failed: {e}")
