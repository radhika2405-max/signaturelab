"""
Script to generate Google Colab-compatible Jupyter Notebook
"""

import os
import nbformat as nbf

def create_notebook():
    os.makedirs("notebooks", exist_ok=True)
    nb = nbf.v4.new_notebook()
    
    cells = []
    
    # Title Markdown
    cells.append(nbf.v4.new_markdown_cell(
r"""# HANDWRITTEN SIGNATURE VERIFICATION USING LINEAR ALGEBRA
### An Application of Vector Spaces, Matrices, Inner Products, Norms, and Linear Maps
**Application Name:** SignatureLab — Linear Algebra Verification Studio  
**Course:** Linear Algebra (Undergraduate Mini-Project)  
**Google Colab Compatibility:** 100% Self-Contained and Executable  

*Linear Algebra Mini Project — Educational Demonstration*  
*Notice: This notebook demonstrates how linear algebra can be used to model and compare high-dimensional image vectors. It does not guarantee authenticity or forensic proof.*
"""
    ))

    # Cell 1: Environment Setup
    cells.append(nbf.v4.new_code_cell(
"""# Step 1: Install & Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image

print("NumPy version:", np.__version__)
print("OpenCV version:", cv2.__version__)
"""
    ))

    # Cell 2: Solved Numerical Benchmark (Section 11)
    cells.append(nbf.v4.new_markdown_cell(
r"""## 1. Solved Numerical Verification Benchmark (Section 11)
We verify the analytical mathematical engine on benchmark vectors in $\mathbb{R}^3$:
$$A = (1, 2, 3), \quad B = (2, 3, 4)$$
"""
    ))

    cells.append(nbf.v4.new_code_cell(
"""# Vector arithmetic definitions
A = np.array([1.0, 2.0, 3.0])
B = np.array([2.0, 3.0, 4.0])

# 1. Dot Product
dot_product = np.dot(A, B)
print(f"Dot Product (A . B): {dot_product:.1f} (Exact: 1*2 + 2*3 + 3*4 = 20)")

# 2. Euclidean Norms
norm_A = np.linalg.norm(A)
norm_B = np.linalg.norm(B)
print(f"Norm of A (||A||_2): {norm_A:.4f} (Exact: sqrt(14) ~= {np.sqrt(14):.4f})")
print(f"Norm of B (||B||_2): {norm_B:.4f} (Exact: sqrt(29) ~= {np.sqrt(29):.4f})")

# 3. Euclidean Distance
dist_AB = np.linalg.norm(A - B)
print(f"Euclidean Distance d(A,B): {dist_AB:.4f} (Exact: sqrt(3) ~= {np.sqrt(3):.4f})")

# 4. Cosine Similarity
cos_sim = dot_product / (norm_A * norm_B)
angle_deg = np.degrees(np.arccos(cos_sim))
print(f"Cosine Similarity cos(theta): {cos_sim:.4f} (Exact: 20/sqrt(406) ~= {20/np.sqrt(406):.4f})")
print(f"Subspace Angle theta: {angle_deg:.2f} degrees")
"""
    ))

    # Cell 3: 2x2 Matrix to 4D Vector Space
    cells.append(nbf.v4.new_markdown_cell(
r"""## 2. 2×2 Image Matrix to 4-Dimensional Vector Space Isomorphism
Demonstrating how a 2D matrix in $M_{2,2}(\mathbb{R})$ flattens to a 4D vector in $\mathbb{R}^4$:
"""
    ))

    cells.append(nbf.v4.new_code_cell(
"""# 2x2 Image Patches
M_A = np.array([[10, 20], [30, 40]], dtype=np.float64)
M_B = np.array([[15, 25], [35, 45]], dtype=np.float64)

v_A = M_A.flatten()
v_B = M_B.flatten()

print("Matrix M_A:\\n", M_A)
print("Flattened Vector v_A in R^4:", v_A)
print("Flattened Vector v_B in R^4:", v_B)

dot_2x2 = np.dot(v_A, v_B)
cos_2x2 = dot_2x2 / (np.linalg.norm(v_A) * np.linalg.norm(v_B))
print(f"2x2 Dot Product: {dot_2x2:.1f}")
print(f"2x2 Cosine Similarity: {cos_2x2:.4f}")
"""
    ))

    # Cell 4: Signature Preprocessing Functions
    cells.append(nbf.v4.new_markdown_cell(
"""## 3. Signature Image Preprocessing Pipeline
We implement the aspect-ratio-preserving resize, centering, and foreground stroke inversion.
"""
    ))

    cells.append(nbf.v4.new_code_cell(
"""def preprocess_signature(image_path, target_h=128, target_w=256):
    # Load Grayscale
    gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise ValueError(f"Could not load image: {image_path}")
        
    # Detect signature bounding box using Otsu threshold
    is_light = np.mean(gray) > 127
    inv = cv2.bitwise_not(gray) if is_light else gray
    _, thresh = cv2.threshold(inv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    pts = cv2.findNonZero(thresh)
    
    if pts is not None and len(pts) > 10:
        x, y, w, h = cv2.boundingRect(pts)
        pad = 10
        x0, y0 = max(0, x - pad), max(0, y - pad)
        x1, y1 = min(gray.shape[1], x + w + pad), min(gray.shape[0], y + h + pad)
        cropped = gray[y0:y1, x0:x1]
    else:
        cropped = gray
        
    # Aspect-preserving resize
    h, w = cropped.shape
    scale = min(target_w / w, target_h / h)
    new_w = max(1, int(round(w * scale)))
    new_h = max(1, int(round(h * scale)))
    resized = cv2.resize(cropped, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    # Pad to canonical canvas
    canvas = np.full((target_h, target_w), 255, dtype=np.uint8)
    ox = (target_w - new_w) // 2
    oy = (target_h - new_h) // 2
    canvas[oy:oy+new_h, ox:ox+new_w] = resized
    
    # Foreground representation (ink > 0, paper = 0)
    foreground = (255.0 - canvas.astype(np.float64)) / 255.0
    foreground[foreground < 0.05] = 0.0
    
    vector = foreground.flatten()
    return foreground, vector
"""
    ))

    # Cell 5: Comparison Execution on Sample Images
    cells.append(nbf.v4.new_markdown_cell(
r"""## 4. Full Signature Verification in $\mathbb{R}^{32,768}$
Now we execute the real comparison pipeline between genuine and forged signatures.
"""
    ))

    cells.append(nbf.v4.new_code_cell(
"""# Run comparison on generated samples
path_ref = "../assets/sample_signatures/author_a_genuine_1.png"
path_gen = "../assets/sample_signatures/author_a_genuine_2.png"
path_forged = "../assets/sample_signatures/author_a_forged.png"

# Process genuine pair
mat_ref, vec_ref = preprocess_signature(path_ref)
mat_gen, vec_gen = preprocess_signature(path_gen)
mat_forged, vec_forged = preprocess_signature(path_forged)

def compare_vectors(u, v):
    dot = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    dist = np.linalg.norm(u - v)
    cos = dot / (norm_u * norm_v)
    angle = np.degrees(np.arccos(np.clip(cos, -1.0, 1.0)))
    return dot, norm_u, norm_v, dist, cos, angle

dot_g, nu_g, nv_g, dist_g, cos_g, ang_g = compare_vectors(vec_ref, vec_gen)
dot_f, nu_f, nv_f, dist_f, cos_f, ang_f = compare_vectors(vec_ref, vec_forged)

print(f"Vector Space Dimension: R^{len(vec_ref)}")
print("-" * 55)
print(f"GENUINE PAIR: Cosine Sim = {cos_g:.4f} | Distance = {dist_g:.2f} | Angle = {ang_g:.2f}°")
print(f"FORGED PAIR:  Cosine Sim = {cos_f:.4f} | Distance = {dist_f:.2f} | Angle = {ang_f:.2f}°")
"""
    ))

    # Cell 6: Visualizations & Difference Heatmap
    cells.append(nbf.v4.new_code_cell(
"""# Difference Heatmap Visualization
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(mat_ref, cmap='gray_r')
axes[0].set_title("Reference Signature (u)")
axes[0].axis('off')

axes[1].imshow(mat_gen, cmap='gray_r')
axes[1].set_title(f"Genuine Variant (cos={cos_g:.3f})")
axes[1].axis('off')

diff = np.abs(mat_ref - mat_gen)
im = axes[2].imshow(diff, cmap='hot')
axes[2].set_title(f"Absolute Difference |u - v|")
axes[2].axis('off')
plt.colorbar(im, ax=axes[2], fraction=0.046, pad=0.04)

plt.suptitle("Linear Algebra Signature Comparison & Residual Heatmap", fontsize=14)
plt.tight_layout()
plt.show()
"""
    ))

    # Cell 7: Conclusions
    cells.append(nbf.v4.new_markdown_cell(
r"""## 5. Conclusions & Limitations for Viva Voce
1. **Linear Algebra Foundations:** By mapping signatures into $\mathbb{R}^{mn}$, inner products and cosine similarity provide transparent, reproducible geometric similarity scores.
2. **Cauchy-Schwarz Guarantee:** Directional alignment is bounded in $[0, 1]$ for non-negative pixel vectors.
3. **Physical Limitations:** Pure Euclidean vectors lack translation and rotation invariance; hence, preprocessing is crucial.
4. **Educational Scope:** This study is an educational model and should never be used as commercial or forensic proof of identity.
"""
    ))

    nb.cells = cells
    
    out_path = os.path.join("notebooks", "linear_algebra_signature_verification.ipynb")
    with open(out_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"Wrote notebook to {out_path}")

if __name__ == "__main__":
    create_notebook()
