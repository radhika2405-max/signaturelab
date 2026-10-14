# Sample Signature Benchmark Dataset
### Linear Algebra Signature Verification Mini-Project

## 1. Dataset Origin & Provenance
To respect human biometric privacy in compliance with institutional ethics (Section 16), this evaluation dataset contains clean, synthetically generated high-resolution signature samples simulating genuine intra-writer variations and skilled forgeries:
- **Author A ("Alex Carter"):** Cursive flourish style with dynamic diagonal crossbars.
  - `author_a_genuine_1.png`: Reference signature sample.
  - `author_a_genuine_2.png`: Genuine secondary sample featuring natural biological motor noise, slight velocity variance, and minor stroke shifting.
  - `author_a_forged.png`: Simulated skilled forgery mimicking letter contours with tremor and geometric distortions.
- **Author B ("Sophia Miller"):** Looping circular signature style.
  - `author_b_genuine_1.png`: Reference signature sample.
  - `author_b_genuine_2.png`: Genuine secondary variant.

## 2. Metadata File: `pairs.csv`
Structure conforming to Section 14:
```csv
pair_id,reference_image,test_image,pair_label
1,author_a_genuine_1.png,author_a_genuine_2.png,Author A: Genuine vs Genuine
2,author_a_genuine_1.png,author_a_forged.png,Author A: Genuine vs Skilled Forgery
3,author_b_genuine_1.png,author_b_genuine_2.png,Author B: Genuine vs Genuine
4,author_a_genuine_1.png,author_b_genuine_1.png,Author A vs Author B (Cross-Writer 1)
5,author_a_genuine_2.png,author_b_genuine_2.png,Author A vs Author B (Cross-Writer 2)
6,author_b_genuine_1.png,author_a_forged.png,Author B vs Author A Forgery
```

## 3. Privacy & Storage Notice
All images are processed strictly in-memory (RAM) during active Streamlit sessions and are not uploaded to any remote server or persistent database.
