import sys
import os

# Ensure Python can find `src/`
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

print("🚀 Running deploy.py (simplified)")

# Test simple import
try:
    import deployment_orchestrator
    print("✅ Successfully imported deployment_orchestrator")
except ImportError as e:
    print(f"❌ Failed to import deployment_orchestrator: {e}")

def main():
    print("✅ Running main deployment logic...")

if __name__ == "__main__":
    main()
