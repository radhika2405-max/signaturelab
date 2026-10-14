#!/usr/bin/env bash
# ======================================================================
# SignatureLab: AI-Assisted Handwritten Signature Comparison
# 1-Click Offline Preview (macOS / Linux)
# ======================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================================"
echo "   SignatureLab: AI-Assisted Handwritten Signature Comparison"
echo "   1-Click Offline Preview"
echo "======================================================================"
echo ""

# Open index.html in default browser
if command -v xdg-open &>/dev/null; then
    xdg-open "$SCRIPT_DIR/index.html"
elif command -v open &>/dev/null; then
    open "$SCRIPT_DIR/index.html"
else
    echo "Please open $SCRIPT_DIR/index.html in your web browser."
fi

# Also launch Python runner if available
if command -v python3 &>/dev/null; then
    python3 run.py &
elif command -v python &>/dev/null; then
    python run.py &
fi
