"""
Test utility functions
"""

import unittest
import sys
from pathlib import Path
import tempfile

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from utils import (
    get_file_size,
    generate_hash,
    sanitize_filename,
    get_timestamp,
    format_duration,
    ensure_dir
)

class TestUtils(unittest.TestCase):
    """Test utility functions"""
    
    def test_generate_hash(self):
        """Test hash generation"""
        hash1 = generate_hash("test")
        hash2 = generate_hash("test")
        self.assertEqual(hash1, hash2)
        
        hash3 = generate_hash("different")
        self.assertNotEqual(hash1, hash3)
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        dirty = "file<name>:test.mp4"
        clean = sanitize_filename(dirty)
        self.assertNotIn("<", clean)
        self.assertNotIn(">", clean)
        self.assertNotIn(":", clean)
    
    def test_get_timestamp(self):
        """Test timestamp generation"""
        timestamp = get_timestamp()
        self.assertIsInstance(timestamp, str)
        self.assertEqual(len(timestamp), 15)  # YYYYMMDD_HHMMSS
    
    def test_format_duration(self):
        """Test duration formatting"""
        self.assertEqual(format_duration(30), "30.0s")
        self.assertEqual(format_duration(90), "1m 30s")
    
    def test_ensure_dir(self):
        """Test directory creation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / "test" / "nested"
            result = ensure_dir(test_dir)
            self.assertTrue(result.exists())
            self.assertTrue(result.is_dir())

if __name__ == '__main__':
    unittest.main()
