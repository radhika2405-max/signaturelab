"""
Unit tests for src.comparison module
Verifies comparison pipeline, threshold boundary conditions, and decision logic.
"""

import pytest
import os
import numpy as np
from src.comparison import compare_signatures


def test_compare_signatures_genuine_and_forged():
    """
    Tests end-to-end comparison on genuine and forged sample files.
    """
    ref_path = "sample_data/author_a_genuine_1.png"
    gen_path = "sample_data/author_a_genuine_2.png"
    forged_path = "sample_data/author_a_forged.png"
    
    assert os.path.exists(ref_path)
    assert os.path.exists(gen_path)
    assert os.path.exists(forged_path)
    
    res_gen = compare_signatures(ref_path, gen_path, similarity_threshold=0.60)
    res_forged = compare_signatures(ref_path, forged_path, similarity_threshold=0.60)
    
    assert res_gen["similarity_decision"] is True
    assert res_forged["similarity_decision"] is False
    assert res_gen["metrics"]["cosine_similarity"] > res_forged["metrics"]["cosine_similarity"]
    assert res_gen["metrics"]["euclidean_distance"] < res_forged["metrics"]["euclidean_distance"]
