"""
Health check script for NEXUS VISION
Verifies system status and dependencies
"""

import sys
import requests
from pathlib import Path

def check_server():
    """Check if server is running"""
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is running")
            print(f"   Status: {data.get('status')}")
            print(f"   Method: {data.get('method')}")
            return True
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required = ['fastapi', 'uvicorn', 'moviepy', 'requests']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    return len(missing) == 0

def check_directories():
    """Check if required directories exist"""
    base_dir = Path(__file__).parent.parent
    required_dirs = [
        base_dir / "backend",
        base_dir / "frontend",
        base_dir / "outputs",
        base_dir / "outputs" / "clips",
        base_dir / "outputs" / "videos"
    ]
    
    all_exist = True
    for directory in required_dirs:
        if directory.exists():
            print(f"✅ {directory.name} exists")
        else:
            print(f"❌ {directory.name} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all health checks"""
    print("🏥 NEXUS VISION Health Check")
    print("=" * 50)
    
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n📁 Checking directories...")
    dirs_ok = check_directories()
    
    print("\n🌐 Checking server...")
    server_ok = check_server()
    
    print("\n" + "=" * 50)
    if deps_ok and dirs_ok and server_ok:
        print("✅ All checks passed!")
        sys.exit(0)
    else:
        print("❌ Some checks failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
