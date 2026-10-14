# Unit-Wise Syllabus Mapping Table
### Comprehensive Linear Algebra Curriculum Mapping

| Unit | Mathematical Concept | Project Application | Actual Implementation Status | Explanation / Evidence |
| :--- | :--- | :--- | :--- | :--- |
| **Unit 1** | Real Vector Space $M_{m,n}(\mathbb{R})$ | Canonical $128 \times 256$ image matrix | Directly Implemented | Standardized canvas satisfies all 8 vector space axioms under matrix addition and scalar multiplication. |
| **Unit 1** | Vectors in $\mathbb{R}^N$ | Flattened 1D signature embedding | Directly Implemented | $v = \text{vec}(M) \in \mathbb{R}^{32,768}$. Implemented in `src/vector_math.py`. |
| **Unit 1** | Basis and Dimension | Standard basis $\{e_i\}$ of $\mathbb{R}^{mn}$ | Directly Implemented | $\dim(V) = 32,768$; standard basis consists of single-pixel impulse matrices $E_{ij}$. |
| **Unit 1** | Linear Independence | Distinct signatures as independent vectors | Directly Implemented | Signatures of different authors are non-collinear ($\cos \theta < 0.60$). |
| **Unit 1** | Subspaces & Sums | Subspace of $128 \times 256$ digital images | Directly Implemented | Fixed canvas signatures form a linear subspace within arbitrary digital images. |
| **Unit 2** | Linear Maps | Grayscale luminance conversion | Directly Implemented | $Y = 0.299R + 0.587G + 0.114B$ is a linear projection $\mathbb{R}^3 \to \mathbb{R}$. |
| **Unit 2** | Isomorphisms | Matrix vectorization $\text{vec}$ | Directly Implemented | Bijective linear map preserving vector operations. |
| **Unit 2** | Rank-Nullity Theorem | Orthogonal projection operators | Directly Implemented | $\text{proj}_v(u)$ has rank 1 and nullity $N-1$; satisfies $\dim(\text{im}) + \dim(\ker) = N$. |
| **Unit 2** | Nonlinear Operators | Otsu thresholding & margin cropping | Directly Implemented & Contrast Analyzed | Clarified that thresholding and min/max cropping are non-linear. |
| **Unit 3** | Euclidean Inner Product | Dot product $\langle u, v \rangle = \sum u_i v_i$ | Directly Implemented | Evaluates spatial overlap. Hand-verified with benchmark $A=(1,2,3), B=(2,3,4)$ giving 20. |
| **Unit 3** | Euclidean Norm | $L_2$ norm $\|u\|_2 = \sqrt{\langle u, u \rangle}$ | Directly Implemented | Measures total ink mass. Hand-verified $\|A\|=\sqrt{14}, \|B\|=\sqrt{29}$. |
| **Unit 3** | Euclidean Distance | Metric $d(u, v) = \|u - v\|_2$ | Directly Implemented | Point-to-point distance in $\mathbb{R}^N$. Hand-verified $d(A,B)=\sqrt{3} \approx 1.732$. |
| **Unit 3** | Cosine Similarity | Directional alignment $\cos(\theta)$ | Directly Implemented | Scale-invariant similarity bounded in $[0, 1]$ via Cauchy-Schwarz inequality. |
| **Unit 3** | Eigenvalues & Eigenvectors | Covariance matrix decomposition (PCA) | Genuinely Implemented & Visualized | Solves $C v_k = \lambda_k v_k$ in `src/vector_math.py`. |
