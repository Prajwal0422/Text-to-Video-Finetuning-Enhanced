"""
GPU Utilities
CUDA detection and GPU-accelerated operations
"""

import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)


class GPUManager:
    """Manage GPU resources and operations"""
    
    def __init__(self):
        self.cuda_available = self._check_cuda()
        self.device_count = self._get_device_count()
        
        if self.cuda_available:
            logger.info(f"✅ GPU acceleration enabled ({self.device_count} device(s))")
        else:
            logger.info("⚠️  GPU acceleration not available, using CPU")
    
    def _check_cuda(self) -> bool:
        """Check if CUDA is available"""
        try:
            return cv2.cuda.getCudaEnabledDeviceCount() > 0
        except:
            return False
    
    def _get_device_count(self) -> int:
        """Get number of CUDA devices"""
        try:
            return cv2.cuda.getCudaEnabledDeviceCount()
        except:
            return 0
    
    def upload_frame(self, frame: np.ndarray):
        """Upload frame to GPU memory"""
        if self.cuda_available:
            return cv2.cuda_GpuMat(frame)
        return frame
    
    def download_frame(self, gpu_frame) -> np.ndarray:
        """Download frame from GPU memory"""
        if self.cuda_available and hasattr(gpu_frame, 'download'):
            return gpu_frame.download()
        return gpu_frame
    
    def resize_gpu(self, frame: np.ndarray, size: tuple) -> np.ndarray:
        """GPU-accelerated resize"""
        if self.cuda_available:
            try:
                gpu_frame = cv2.cuda_GpuMat(frame)
                gpu_resized = cv2.cuda.resize(gpu_frame, size)
                return gpu_resized.download()
            except:
                pass
        
        return cv2.resize(frame, size, interpolation=cv2.INTER_LANCZOS4)
    
    def convert_color_gpu(self, frame: np.ndarray, code: int) -> np.ndarray:
        """GPU-accelerated color conversion"""
        if self.cuda_available:
            try:
                gpu_frame = cv2.cuda_GpuMat(frame)
                gpu_converted = cv2.cuda.cvtColor(gpu_frame, code)
                return gpu_converted.download()
            except:
                pass
        
        return cv2.cvtColor(frame, code)
    
    def get_device_info(self) -> dict:
        """Get GPU device information"""
        if not self.cuda_available:
            return {"available": False}
        
        try:
            info = {
                "available": True,
                "device_count": self.device_count,
                "devices": []
            }
            
            for i in range(self.device_count):
                cv2.cuda.setDevice(i)
                device_info = {
                    "id": i,
                    "name": cv2.cuda.getDevice(),
                }
                info["devices"].append(device_info)
            
            return info
        except:
            return {"available": True, "device_count": self.device_count}


# Global GPU manager instance
_gpu_manager = None


def get_gpu_manager() -> GPUManager:
    """Get global GPU manager instance"""
    global _gpu_manager
    if _gpu_manager is None:
        _gpu_manager = GPUManager()
    return _gpu_manager


def is_gpu_available() -> bool:
    """Check if GPU is available"""
    return get_gpu_manager().cuda_available
