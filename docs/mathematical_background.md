# Mathematical Background
### Units 1, 2, and 3 Syllabus Foundations

## Unit 1: Introduction to Vector Spaces
- **Vector Space Axioms:** A set $V$ with operations $(+)$ and $(\cdot)$ over $\mathbb{R}$.
- **Matrix Space:** $M_{m,n}(\mathbb{R})$ is an $mn$-dimensional real vector space.
- **Isomorphism:** The map $\text{vec}: M_{m,n}(\mathbb{R}) \to \mathbb{R}^{mn}$ satisfies:
  $$\text{vec}(A + B) = \text{vec}(A) + \text{vec}(B)$$
  $$\text{vec}(\alpha A) = \alpha \, \text{vec}(A)$$
  with $\ker(\text{vec}) = \{\mathbf{0}\}$, establishing $M_{m,n}(\mathbb{R}) \cong \mathbb{R}^{mn}$.
- **Basis and Dimension:** $\dim(V) = mn = 32,768$. Standard basis $\{e_1, e_2, \dots, e_{32768}\}$.

## Unit 2: Linear Maps
- **Linearity Conditions:** $T(u + v) = T(u) + T(v)$ and $T(\alpha u) = \alpha T(u)$.
- **Luminance Projection:** Grayscale conversion $Y = 0.299R + 0.587G + 0.114B$ is a linear projection $\mathbb{R}^3 \to \mathbb{R}$.
- **Orthogonal Projection:** $\text{proj}_v(u) = \frac{\langle u, v \rangle}{\|v\|^2} v$. Rank = 1, Nullity = $N-1$.
- **Nonlinear Distinctions:** Thresholding (step function) and bounding box cropping are strictly nonlinear.

## Unit 3: Eigenvalues, Eigenvectors, and Inner Product Spaces
- **Euclidean Inner Product:** $\langle u, v \rangle = \sum_{i=1}^N u_i v_i$.
- **Norm and Metric Distance:** $\|u\|_2 = \sqrt{\sum u_i^2}$, $d(u, v) = \|u - v\|_2$.
- **Cauchy-Schwarz Theorem:** $|\langle u, v \rangle| \le \|u\|_2 \|v\|_2$.
- **Cosine Similarity:** $\cos(\theta) = \frac{u \cdot v}{\|u\|_2 \|v\|_2}$.
- **Covariance Eigendecomposition:** Solves $C v_k = \lambda_k v_k$ to find principal axes of handwriting variance.
