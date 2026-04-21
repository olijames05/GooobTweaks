"""
Build script to create a standalone executable for WinTweaks.
Uses PyInstaller to bundle the application.
"""

import sys
import os
import subprocess
import shutil


def main():
    """Build the WinTweaks executable."""
    
    print("WinTweaks Builder")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")
    
    # Clean previous builds
    if os.path.exists("build"):
        print("Cleaning previous build...")
        shutil.rmtree("build")
    
    if os.path.exists("dist"):
        print("Cleaning previous dist...")
        shutil.rmtree("dist")
    
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=WinTweaks",
        "--onefile",
        "--windowed",
        "--icon=NONE",
        "--clean",
        "--noconfirm",
        "--add-data", "src;src",
        "--hidden-import", "winreg",
        "--hidden-import", "ctypes",
        "main.py"
    ]
    
    print("\nBuilding executable...")
    print("This may take a few minutes...")
    print("-" * 50)
    
    try:
        subprocess.check_call(cmd)
        print("-" * 50)
        print("✓ Build successful!")
        print(f"\nExecutable location: {os.path.abspath('dist/WinTweaks.exe')}")
        print("\nNote: Run the executable as Administrator for full functionality.")
        return 0
    except subprocess.CalledProcessError as e:
        print("-" * 50)
        print(f"✗ Build failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
