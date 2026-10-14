# SignatureLab
### AI-Assisted Handwritten Signature Comparison
**Tagline:** Compare handwritten signatures in seconds.

---

## 📌 Overview

**SignatureLab** is a focused, modern application designed to compare two handwritten signature images and help users determine whether they are sufficiently similar under a clearly defined mathematical comparison pipeline.

Built for fast, intuitive, and private signature comparison, SignatureLab processes images entirely in-memory on your local machine, without sending data to external cloud services.

---

## 🚀 Key Features

- **Side-by-Side Signature Upload:** Drag-and-drop or browse Reference and Test signature images (PNG, JPG, JPEG).
- **Instant Sample Benchmarks:** One-click presets to test genuine pairs, skilled forgeries, and cross-author pairs.
- **Robust Preprocessing Pipeline:**
  1. Grayscale luminance conversion ($Y = 0.299R + 0.587G + 0.114B$)
  2. Blank paper & uniform image detection
  3. Otsu-based bounding box stroke extraction & blank margin removal
  4. Aspect-ratio-preserving proportional resize
  5. Canonical centered canvas padding ($128 \times 256$)
  6. Normalized foreground stroke representation ($[0.0, 1.0]$)
- **Mathematical Comparison Engine:**
  - **Cosine Similarity:** Measures directional stroke alignment ($\cos\theta \in [0, 1]$).
  - **Euclidean Distance:** Quantifies numerical $L_2$ difference between preprocessed image vectors ($d(u,v) = \|u - v\|_2$).
- **Simple, Clear Results:**
  - Clear categorical outcomes: *High Similarity*, *Moderate Similarity*, *Low Similarity*, or *Unable to Compare*.
  - Plain-language result summaries.
  - Spatial difference heatmap highlighting coordinate discrepancies between ink strokes.
- **Privacy First:** In-memory image processing; no permanent disk storage or cloud exposure.

---

## ⚙️ Quick Start Guide (Runs on Any System)

### Option A: Windows (1-Click)
Simply **double-click** [`run_app.bat`](file:///c:/Users/Hp/Downloads/linear%20mini%20project/run_app.bat).
* It automatically detects Python, installs missing libraries if needed, finds an available port, launches the app, and opens your browser!

### Option B: Universal Python (Windows, macOS, Linux)
Open your terminal in this folder and run:
```bash
python run.py
```
*(On macOS/Linux you can also use `python3 run.py` or `./run_app.sh`)*

### Option C: Docker (Zero-Install)
If you have Docker installed, simply run:
```bash
docker compose up
```
Open your browser to: **`http://localhost:8501`**

---

## 🔬 How the Comparison Engine Works

1. **Image Validation:** Validates image format and ensures input is not blank or uniform.
2. **Margin Cropping & Aspect-Preserving Normalization:** Crops excessive blank margins around ink strokes while strictly preserving signature aspect ratio.
3. **Canvas Centering:** Centers the signature inside a fixed standard canvas ($128 \times 256$ pixels).
4. **Vector Flattening:** Flattens the $128 \times 256$ matrix into a $32,768$-dimensional vector $u, v \in \mathbb{R}^{32,768}$.
5. **Metric Evaluation:**
   - **Cosine Similarity:**
     $$\cos(\theta) = \frac{\langle u, v \rangle}{\|u\|_2 \|v\|_2}$$
   - **Euclidean Distance:**
     $$d(u, v) = \|u - v\|_2 = \sqrt{\sum_{i=1}^N (u_i - v_i)^2}$$
6. **Provisional Interpretation:** Scores above threshold $\tau \ge 0.70$ indicate strong numerical stroke alignment, while scores below $0.50$ indicate significant structural divergence.

> **Important Notice:** SignatureLab provides numerical similarity metrics between digital images. Numerical similarity does not constitute legal, forensic, or certified proof of biometric identity or signature authenticity.

---

## 🧪 Testing

To run the automated test suite (45 unit and integration tests):
```powershell
python -m pytest tests/ -v
```
