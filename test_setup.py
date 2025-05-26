import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10 or higher is required")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def check_required_files():
    print("\nChecking required files...")
    required_files = [
        "pokedex_dataset_ready",
        "pokedex_model.h5",
        "requirements.txt",
        "backend/backend.py",
        "frontend/package.json"
    ]
    
    all_present = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ Found {file}")
        else:
            print(f"❌ Missing {file}")
            all_present = False
    
    return all_present

def check_dependencies():
    print("\nChecking Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False

def check_node_modules():
    print("\nChecking Node.js dependencies...")
    if not os.path.exists("frontend/node_modules"):
        print("❌ node_modules not found. Please run 'npm install' in the frontend directory")
        return False
    print("✅ node_modules found")
    return True

def main():
    print("Starting setup verification...\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Files", check_required_files),
        ("Python Dependencies", check_dependencies),
        ("Node.js Dependencies", check_node_modules)
    ]
    
    all_passed = True
    for name, check in checks:
        print(f"\n=== {name} ===")
        if not check():
            all_passed = False
    
    print("\n=== Final Results ===")
    if all_passed:
        print("✅ All checks passed! The setup is complete.")
        print("\nTo start the application:")
        print("1. Start the backend: cd backend && python backend.py")
        print("2. Start the frontend: cd frontend && npm run dev")
    else:
        print("❌ Some checks failed. Please fix the issues above.")

if __name__ == "__main__":
    main() 