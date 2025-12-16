import subprocess
import sys

if __name__ == "__main__":
    subprocess.Popen([
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--reload"
    ])

    subprocess.Popen([
        sys.executable, "-m", "streamlit",
        "run", "frontend/dashboard.py"
    ])
