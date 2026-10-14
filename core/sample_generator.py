"""
SignatureLab — Sample Signature Generator
Creates realistic synthetic signature images for instant academic demonstration and testing.
Includes genuine signature variants, forgeries, and distinct writers.
"""

import os
from pathlib import Path
import numpy as np
import cv2


def draw_smooth_signature(
    strokes: list,
    width: int = 500,
    height: int = 250,
    thickness: int = 3,
    noise_level: float = 0.5
) -> np.ndarray:
    """
    Renders realistic handwritten strokes on a clean white paper canvas with antialiasing.
    """
    canvas = np.full((height, width, 3), 255, dtype=np.uint8)
    
    for stroke in strokes:
        pts = []
        for (x, y) in stroke:
            # Add minor natural human jitter
            jx = x + np.random.normal(0, noise_level)
            jy = y + np.random.normal(0, noise_level)
            pts.append([int(round(jx)), int(round(jy))])
        
        pts = np.array(pts, dtype=np.int32).reshape((-1, 1, 2))
        
        # Draw smooth polyline with dark ink color
        ink_color = (20, 25, 45)  # dark blue-black ink
        cv2.polylines(canvas, [pts], isClosed=False, color=ink_color, thickness=thickness, lineType=cv2.LINE_AA)
        
    return canvas


def _save_image(path: str, img: np.ndarray) -> None:
    """Saves image safely supporting non-ASCII / Unicode paths cross-platform."""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    is_success, buf = cv2.imencode(".png", img)
    if is_success:
        with open(path, "wb") as f:
            f.write(buf.tobytes())
    else:
        cv2.imwrite(path, img)


def generate_all_sample_signatures(output_dir: str = "assets/sample_signatures") -> dict:
    """
    Generates realistic sample signatures for demonstration:
    - Author A: Genuine 1, Genuine 2, Forgery
    - Author B: Genuine 1, Genuine 2
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    np.random.seed(42)

    # Base strokes for Author A ("Alex Carter")
    author_a_base = [
        # Large flourish A
        [(70, 180), (85, 120), (105, 60), (125, 130), (145, 190)],
        # Crossbar & loop
        [(85, 140), (135, 135), (150, 100), (170, 150)],
        # Quick cursive body
        [(170, 150), (190, 135), (205, 160), (220, 130), (240, 165), (260, 130), (280, 155)],
        # Tail underline flourish
        [(140, 200), (220, 205), (320, 195), (410, 185)]
    ]

    # Author A - Genuine Variant 1
    img_a1 = draw_smooth_signature(author_a_base, thickness=3, noise_level=0.3)
    p_a1 = os.path.join(output_dir, "author_a_genuine_1.png")
    _save_image(p_a1, img_a1)

    # Author A - Genuine Variant 2 (natural human intra-person variation: slightly faster, slightly shifted)
    author_a_var2 = []
    for stroke in author_a_base:
        mod_stroke = []
        for x, y in stroke:
            # subtle scale and slight rotation
            nx = (x - 200) * 0.98 + (y - 140) * 0.03 + 205
            ny = -(x - 200) * 0.03 + (y - 140) * 0.98 + 142
            mod_stroke.append((nx, ny))
        author_a_var2.append(mod_stroke)
    img_a2 = draw_smooth_signature(author_a_var2, thickness=3, noise_level=0.8)
    p_a2 = os.path.join(output_dir, "author_a_genuine_2.png")
    _save_image(p_a2, img_a2)

    # Author A - Skilled Forgery (hesitant, irregular jitter, altered proportions)
    author_a_forgery = [
        [(75, 175), (92, 115), (103, 68), (120, 140), (140, 185)],
        [(80, 145), (130, 140), (155, 115), (165, 155)],
        [(165, 155), (185, 145), (198, 165), (215, 140), (245, 170), (270, 140), (295, 160)],
        [(130, 205), (210, 210), (300, 202), (380, 195)]
    ]
    img_af = draw_smooth_signature(author_a_forgery, thickness=4, noise_level=1.8)
    p_af = os.path.join(output_dir, "author_a_forged.png")
    _save_image(p_af, img_af)

    # Author B - Genuine 1 ("Sophia Miller" - looping circular style)
    author_b_base = [
        # Loop S
        [(90, 80), (130, 60), (145, 90), (115, 120), (100, 150), (135, 175), (165, 150)],
        # Sharp connector to M
        [(165, 150), (200, 90), (220, 165), (240, 95), (265, 160)],
        # Elegant tail loop
        [(265, 160), (310, 145), (345, 165), (380, 130), (410, 170), (360, 210), (280, 205)]
    ]
    img_b1 = draw_smooth_signature(author_b_base, thickness=3, noise_level=0.4)
    p_b1 = os.path.join(output_dir, "author_b_genuine_1.png")
    _save_image(p_b1, img_b1)

    # Author B - Genuine Variant 2
    author_b_var2 = []
    for stroke in author_b_base:
        mod_stroke = [(x * 1.02 - 5, y * 0.99 + 2) for x, y in stroke]
        author_b_var2.append(mod_stroke)
    img_b2 = draw_smooth_signature(author_b_var2, thickness=3, noise_level=0.7)
    p_b2 = os.path.join(output_dir, "author_b_genuine_2.png")
    _save_image(p_b2, img_b2)

    return {
        "author_a_genuine_1": p_a1,
        "author_a_genuine_2": p_a2,
        "author_a_forged": p_af,
        "author_b_genuine_1": p_b1,
        "author_b_genuine_2": p_b2,
    }


if __name__ == "__main__":
    generated = generate_all_sample_signatures()
    print("Generated sample signatures successfully:")
    for k, v in generated.items():
        print(f"  {k}: {v}")
