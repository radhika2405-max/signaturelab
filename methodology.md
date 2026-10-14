# Proposed Methodology & Verification Pipeline

## Overview of the Pipeline
The signature verification pipeline transforms analog documents into standardized Euclidean vectors through four core stages:

```
Raw Image ─> Grayscale ─> Bounding Box ─> Aspect Resize ─> Centered Pad ─> Inversion ─> Vectorization ─> Metric Engine
```

### Stage 1: Ingestion & Validation
- Validates file format (PNG, JPG, JPEG).
- Rejects corrupt byte streams, undersized inputs (< 5x5 px), all-white paper, and all-black frames.

### Stage 2: Spatial Normalization
- Detects ink strokes via Otsu binarization to define bounding box $(x, y, w, h)$.
- Adds 10 px safety margin.
- Calculates aspect-preserving scale factor $s = \min(256 / w, 128 / h)$.
- Places scaled signature into center of $128 \times 256$ canvas.

### Stage 3: Foreground Representation
- Inverts grayscale values: $P_{\text{fg}} = (255 - P) / 255$.
- Suppresses paper texture noise below 0.05 to true zero.
- Ensures white paper does not contribute positively to inner products.

### Stage 4: High-Dimensional Metric Calculation
- Flattens into vector $v \in \mathbb{R}^{32,768}$.
- Calculates dot product, $L_2$ norms, Euclidean distance, and cosine similarity.
- Evaluates classification decisions based on configurable thresholds.
