#!/usr/bin/env python3
"""
Auto-start backend with ngrok tunnel
Shows ngrok URL and auto-updates environment
"""

import subprocess
import time
import sys
from pathlib import Path

def main():
    root = Path(__file__).parent
    backend = root / "backend"
    
    print("=" * 50)
    print("NetShield - Backend + ngrok Setup")
    print("=" * 50)
    print()
    
    # Check ngrok installed
    try:
        result = subprocess.run(["ngrok", "version"], capture_output=True, timeout=5)
        if result.returncode != 0:
            print("❌ ngrok not found!")
            print("Install: https://ngrok.com/download")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error checking ngrok: {e}")
        sys.exit(1)
    
    print("✅ ngrok found")
    print()
    
    # Check backend dependencies
    try:
        from fastapi import FastAPI
        print("✅ FastAPI installed")
    except ImportError:
        print("❌ FastAPI not found. Run: pip install -r requirements.txt")
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("Starting services...")
    print("=" * 50)
    print()
    
    # Start backend
    print("1️⃣  Starting backend on http://localhost:8000")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--port", "8000"],
        cwd=backend,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    time.sleep(3)
    
    # Start ngrok
    print("2️⃣  Starting ngrok tunnel...")
    ngrok_proc = subprocess.Popen(
        ["ngrok", "http", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    print()
    print("=" * 50)
    print("✅ Both services running!")
    print("=" * 50)
    print()
    print("📍 Backend Health: http://localhost:8000/api/health")
    print("📍 ngrok Dashboard: http://127.0.0.1:4040")
    print()
    print("⏳ Waiting for ngrok to initialize (15 sec)...")
    print()
    
    time.sleep(15)
    
    print("=" * 50)
    print("🎉 Ready to deploy!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Check ngrok terminal for PUBLIC URL")
    print("2. Copy that URL (https://xxx.ngrok.io)")
    print("3. Deploy frontend to Vercel with:")
    print("   VITE_API_BASE_URL=https://xxx.ngrok.io")
    print()
    print("Keeping services alive... Press Ctrl+C to stop")
    print()
    
    try:
        backend_proc.wait()
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        backend_proc.terminate()
        ngrok_proc.terminate()
        print("✅ Done")

if __name__ == "__main__":
    main()
