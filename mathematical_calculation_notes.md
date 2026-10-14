# Mathematical Calculation Notes & Benchmark Proofs
### SignatureLab — Linear Algebra Verification Studio

## 1. Solved Numerical Benchmark Verification (Section 11 & Section 21)
Given benchmark vectors in Euclidean space $\mathbb{R}^3$:
$$A = \begin{pmatrix} 1 \\ 2 \\ 3 \end{pmatrix}, \quad B = \begin{pmatrix} 2 \\ 3 \\ 4 \end{pmatrix}$$

### A. Dot Product (Standard Inner Product)
$$\langle A, B \rangle = A \cdot B = \sum_{i=1}^3 a_i b_i = (1)(2) + (2)(3) + (3)(4) = 2 + 6 + 12 = \mathbf{20}$$

### B. Euclidean ($L_2$) Norms
$$\|A\|_2 = \sqrt{\langle A, A \rangle} = \sqrt{1^2 + 2^2 + 3^2} = \sqrt{1 + 4 + 9} = \sqrt{14} \approx \mathbf{3.74165738677}$$
$$\|B\|_2 = \sqrt{\langle B, B \rangle} = \sqrt{2^2 + 3^2 + 4^2} = \sqrt{4 + 9 + 16} = \sqrt{29} \approx \mathbf{5.38516480713}$$

### C. Euclidean Metric Distance
$$d(A, B) = \|A - B\|_2 = \sqrt{(1-2)^2 + (2-3)^2 + (3-4)^2} = \sqrt{(-1)^2 + (-1)^2 + (-1)^2} = \sqrt{1 + 1 + 1} = \sqrt{3} \approx \mathbf{1.73205080757}$$

### D. Cosine Similarity & Directional Subspace Angle
$$\cos(\theta) = \frac{A \cdot B}{\|A\|_2 \, \|B\|_2} = \frac{20}{\sqrt{14} \times \sqrt{29}} = \frac{20}{\sqrt{406}} \approx \mathbf{0.99258333397}$$
$$\theta = \arccos(0.99258333397) \text{ rad} \approx 0.121876 \text{ rad} \approx \mathbf{6.983^\circ}$$

---

## 2. Miniature Image Patch: 2×2 Matrix to 4D Vector Space
$$M_A = \begin{pmatrix} 10 & 20 \\ 30 & 40 \end{pmatrix} \in M_{2,2}(\mathbb{R}) \xrightarrow{\text{vec}} v_A = \begin{pmatrix} 10 \\ 20 \\ 30 \\ 40 \end{pmatrix} \in \mathbb{R}^4$$
$$M_B = \begin{pmatrix} 15 & 25 \\ 35 & 45 \end{pmatrix} \in M_{2,2}(\mathbb{R}) \xrightarrow{\text{vec}} v_B = \begin{pmatrix} 15 \\ 25 \\ 35 \\ 45 \end{pmatrix} \in \mathbb{R}^4$$

- **Dot Product:** $\langle v_A, v_B \rangle = 10(15) + 20(25) + 30(35) + 40(45) = 150 + 500 + 1050 + 1800 = \mathbf{3500}$
- **Norm of A:** $\|v_A\|_2 = \sqrt{100 + 400 + 900 + 1600} = \sqrt{3000} \approx \mathbf{54.77225575}$
- **Norm of B:** $\|v_B\|_2 = \sqrt{225 + 625 + 1225 + 2025} = \sqrt{4100} \approx \mathbf{64.03124237}$
- **Distance:** $d(v_A, v_B) = \sqrt{(-5)^2 + (-5)^2 + (-5)^2 + (-5)^2} = \sqrt{4 \times 25} = \sqrt{100} = \mathbf{10.0}$
- **Cosine Similarity:** $\cos(\theta) = \frac{3500}{\sqrt{3000 \times 4100}} = \frac{3500}{\sqrt{12,300,000}} \approx \mathbf{0.997972}$

---

## 3. High-Dimensional Extension: Canonical Signature Vector Space
When extending to a standard signature canvas of $m = 128$ rows and $n = 256$ columns:
$$\dim(V) = 128 \times 256 = \mathbf{32,768} \text{ dimensions}$$
The exact same algebraic laws hold:
- $\langle u, v \rangle = \sum_{i=1}^{32768} u_i v_i$
- $\|u\|_2 = \sqrt{\sum_{i=1}^{32768} u_i^2}$
- $d(u, v) = \sqrt{\sum_{i=1}^{32768} (u_i - v_i)^2}$
- $\cos(\theta) = \frac{\langle u, v \rangle}{\|u\|_2 \|v\|_2} \in [0, 1]$

---

## 4. Covariance Matrix Eigendecomposition (PCA)
For $k$ centered signature vectors $X_c \in \mathbb{R}^{k \times N}$, the sample covariance matrix is:
$$C = \frac{1}{k-1} X_c^T X_c \in \mathbb{R}^{N \times N}$$
Solving the characteristic equation $\det(C - \lambda I) = 0$ yields eigenvalues $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_k \ge 0$ and orthogonal eigenvectors $v_i$.
The proportion of total handwriting variance explained by eigenvector $v_i$ is:
$$\text{Explained Variance Ratio}_i = \frac{\lambda_i}{\sum_{j=1}^k \lambda_j}$$
This provides a rigorous linear algebra tool to analyze the principal axes of variation in handwritten signatures.
