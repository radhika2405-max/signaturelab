#!/usr/bin/env bash
# ======================================================================
# SignatureLab: AI-Assisted Handwritten Signature Comparison
# macOS & Linux Launcher
# ======================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================================"
echo "   ✍️  SignatureLab: AI-Assisted Handwritten Signature Comparison"
echo "   macOS & Linux Launcher"
echo "======================================================================"
echo ""

# Find Python 3
PYTHON_BIN=""
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    # Verify it's Python 3
    VER=$(python -c 'import sys; print(sys.version_info[0])' 2>/dev/null || echo "0")
    if [ "$VER" -ge 3 ]; then
        PYTHON_BIN="python"
    fi
fi

if [ -z "$PYTHON_BIN" ]; then
    echo "❌ Error: Python 3 was not found."
    echo "   Please install Python 3:"
    echo "   • On macOS: brew install python3"
    echo "   • On Ubuntu/Debian: sudo apt update && sudo apt install -y python3 python3-pip python3-venv"
    echo "   • On Fedora: sudo dnf install -y python3 python3-pip"
    exit 1
fi

echo "✅ Using Python: $($PYTHON_BIN --version)"
echo "🚀 Launching universal runner (run.py)..."
echo ""

exec "$PYTHON_BIN" run.py "$@"
