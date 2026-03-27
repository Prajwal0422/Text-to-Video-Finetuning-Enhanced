"""CLI Interface"""
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m backend.cli <command>")
        return
    
    command = sys.argv[1]
    
    if command == "generate":
        prompt = sys.argv[2] if len(sys.argv) > 2 else "default"
        print(f"Generating: {prompt}")
    elif command == "version":
        print("v2.0.0")
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
