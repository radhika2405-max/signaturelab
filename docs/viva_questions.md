# Comprehensive Viva Voce Examination Questions & Model Answers

### Q1. Why did you choose Cosine Similarity over Euclidean Distance?
**Answer:**  
Euclidean distance $d(u, v) = \|u - v\|_2$ measures absolute point-to-point spatial separation. If an author writes the exact same signature with a thick marker vs a thin pen, the Euclidean distance will be very large due to higher stroke intensity, falsely suggesting an impostor. In contrast, **Cosine Similarity** $\cos(\theta) = \frac{u \cdot v}{\|u\|_2 \|v\|_2}$ is invariant to positive scaling ($u \to \alpha u$). It measures pure directional alignment, capturing the handwriting geometry regardless of pen thickness.

### Q2. What is the dimension of your vector space and how is it derived?
**Answer:**  
Our standardized canvas has dimensions $m = 128$ rows and $n = 256$ columns. The space of all such real matrices is $M_{m,n}(\mathbb{R})$. By applying the lexicographical vectorization isomorphism $\text{vec}: M_{m,n}(\mathbb{R}) \to \mathbb{R}^{mn}$, the dimension is $\dim(V) = 128 \times 256 = 32,768$.

### Q3. Is image preprocessing a linear transformation?
**Answer:**  
No. Grayscale luminance conversion and matrix vectorization are linear mappings. However, Otsu thresholding (binarization) and bounding box cropping are strictly non-linear operations because they rely on variance thresholding and coordinate $\min/\max$ operators that violate additivity $T(u + v) = T(u) + T(v)$.

### Q4. How does the Cauchy-Schwarz inequality apply to your project?
**Answer:**  
The Cauchy-Schwarz theorem states $|\langle u, v \rangle| \le \|u\|_2 \|v\|_2$ for any inner product space. This guarantees that cosine similarity is strictly bounded in $[-1, 1]$. Because our foreground strokes are non-negative ($u_i, v_i \ge 0$), the inner product is non-negative, meaning $\cos(\theta) \in [0, 1]$.

### Q5. What happens if a genuine signature is translated by 10 pixels?
**Answer:**  
Because the standard inner product evaluates $\sum u_i v_i$ at identical coordinate indices $i$, a 10-pixel translation causes the strokes to misalign, making $u_i \times 0 = 0$. The inner product collapses, causing $\cos(\theta)$ to drop significantly. This highlights that pure Euclidean vector spaces lack translation invariance.

### Q6. Walk through the solved numerical benchmark $A=(1,2,3)$ and $B=(2,3,4)$.
**Answer:**  
- **Dot product:** $1(2) + 2(3) + 3(4) = 2 + 6 + 12 = 20$.
- **Norm of A:** $\sqrt{1^2 + 2^2 + 3^2} = \sqrt{14} \approx 3.7417$.
- **Norm of B:** $\sqrt{2^2 + 3^2 + 4^2} = \sqrt{29} \approx 5.3852$.
- **Euclidean distance:** $\sqrt{(1-2)^2 + (2-3)^2 + (3-4)^2} = \sqrt{3} \approx 1.7321$.
- **Cosine similarity:** $\frac{20}{\sqrt{14 \times 29}} = \frac{20}{\sqrt{406}} \approx 0.9926$.
- **Angle:** $\theta = \arccos(0.9926) \approx 6.98^\circ$.

### Q7. How does PCA / Eigendecomposition fit into signature verification?
**Answer:**  
Given multiple signature vectors $X$, the sample covariance matrix is $C = \frac{1}{k-1} X^T X$. Solving the eigenvalue problem $C v_k = \lambda_k v_k$ yields the eigenvectors (principal axes) corresponding to the largest eigenvalues $\lambda_k$. This identifies the directions of maximal handwriting variation.
