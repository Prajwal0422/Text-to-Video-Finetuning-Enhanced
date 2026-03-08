"""
Test configuration module
"""

import unittest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from config import Config

class TestConfig(unittest.TestCase):
    """Test Config class"""
    
    def test_directories_exist(self):
        """Test that required directories exist"""
        self.assertTrue(Config.OUTPUTS_DIR.exists())
        self.assertTrue(Config.CLIPS_DIR.exists())
        self.assertTrue(Config.VIDEOS_DIR.exists())
    
    def test_default_values(self):
        """Test default configuration values"""
        self.assertEqual(Config.PORT, 8000)
        self.assertEqual(Config.DEFAULT_FPS, 30)
        self.assertEqual(Config.DEFAULT_RESOLUTION, 1080)
    
    def test_mode_config(self):
        """Test mode configuration retrieval"""
        fast_config = Config.get_mode_config("fast")
        self.assertIn("max_time", fast_config)
        self.assertIn("quality", fast_config)
    
    def test_has_api_key(self):
        """Test API key check"""
        result = Config.has_api_key()
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()
