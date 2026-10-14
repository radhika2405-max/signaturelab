"""
SignatureLab — Universal 1-Click Launcher
Cross-platform entry point for running the SignatureLab application on Windows, macOS, and Linux.
Automatically checks Python version, verifies/installs dependencies, selects an available port,
launches the Streamlit server, and opens the default web browser.
"""

import sys
import os
import subprocess
import platform
import socket
import time
import webbrowser
import threading


# Configuration
DEFAULT_PORT = 8501
MIN_PYTHON_VERSION = (3, 9)
APP_FILE = "app.py"
REQUIREMENTS_FILE = "requirements.txt"

# Core required modules to check
REQUIRED_PACKAGES = [
    ("streamlit", "streamlit"),
    ("numpy", "numpy"),
    ("cv2", "opencv-python-headless"),
    ("PIL", "pillow"),
    ("pandas", "pandas"),
    ("matplotlib", "matplotlib"),
    ("plotly", "plotly"),
    ("reportlab", "reportlab"),
]


def print_banner():
    banner = r"""
======================================================================
   ✍️  SignatureLab: AI-Assisted Handwritten Signature Comparison
   Universal Cross-Platform Launcher (Windows / macOS / Linux)
======================================================================
"""
    print(banner)


def check_python_version() -> bool:
    """Verifies that running Python meets the minimum version requirement."""
    current = sys.version_info[:2]
    if current < MIN_PYTHON_VERSION:
        print(f"❌ Error: Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ is required.")
        print(f"   Current version: Python {sys.version.split()[0]}")
        print("   Please install a modern version of Python from https://www.python.org/downloads/")
        return False
    print(f"✅ Python Version: {sys.version.split()[0]} ({platform.system()} {platform.machine()})")
    return True


def check_and_install_dependencies() -> bool:
    """Checks for required packages and auto-installs if any are missing."""
    missing = []
    for mod_name, pkg_name in REQUIRED_PACKAGES:
        try:
            __import__(mod_name)
        except ImportError:
            missing.append(pkg_name)

    if not missing:
        print("✅ All required dependencies are installed.")
        return True

    print(f"⚠️  Missing {len(missing)} package(s): {', '.join(missing)}")
    print("⏳ Auto-installing required packages from requirements.txt...")
    print("   This may take a moment on first launch...\n")

    req_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), REQUIREMENTS_FILE)
    if os.path.exists(req_path):
        install_cmd = [sys.executable, "-m", "pip", "install", "-r", req_path]
    else:
        install_cmd = [sys.executable, "-m", "pip", "install"] + missing

    try:
        ret = subprocess.run(install_cmd, check=True)
        print("\n✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to install dependencies automatically (exit code {e.returncode}).")
        print(f"   Please run manually in your terminal:")
        print(f"   {sys.executable} -m pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error installing dependencies: {e}")
        return False


def find_available_port(start_port: int = DEFAULT_PORT, max_attempts: int = 50) -> int:
    """Finds an open TCP port on localhost starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            # Try to bind to test availability
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start_port


def ensure_samples_generated():
    """Generates synthetic benchmark signatures if not already present."""
    try:
        from core.sample_generator import generate_all_sample_signatures
        sample_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample_data")
        os.makedirs(sample_dir, exist_ok=True)
        generate_all_sample_signatures("assets/sample_signatures")
        print("✅ Benchmark signatures verified.")
    except Exception as e:
        print(f"ℹ️  Sample generator note: {e}")


def open_browser_after_delay(url: str, delay_seconds: float = 2.0):
    """Opens browser after server has started up."""
    def _open():
        time.sleep(delay_seconds)
        try:
            webbrowser.open(url)
        except Exception:
            pass
    t = threading.Thread(target=_open, daemon=True)
    t.start()


def run():
    print_banner()

    # Step 1: Check Python version
    if not check_python_version():
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Step 2: Check and install dependencies
    if not check_and_install_dependencies():
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Step 3: Verify samples
    ensure_samples_generated()

    # Step 4: Find available port
    port = find_available_port(DEFAULT_PORT)
    url = f"http://localhost:{port}"

    print("======================================================================")
    print(f"🚀 Starting SignatureLab on: {url}")
    print("   Press Ctrl+C in this terminal at any time to stop the application.")
    print("======================================================================\n")

    # Step 5: Open browser
    open_browser_after_delay(url, delay_seconds=2.0)

    # Step 6: Launch Streamlit
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        APP_FILE,
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--browser.serverAddress",
        "localhost",
        "--theme.base",
        "light",
    ]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n🛑 SignatureLab stopped. Thank you for using SignatureLab!")
    except Exception as e:
        print(f"\n❌ Error launching Streamlit: {e}")
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    run()
