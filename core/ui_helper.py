"""
SignatureLab — UI Helper & Session Management
Provides layout styling, session state initialization, clean product header,
and privacy footer for the signature verification tool.
"""

import os
import streamlit as st


def init_session_state():
    """Initializes global session state variables for SignatureLab."""
    if "comparisons_count" not in st.session_state:
        st.session_state["comparisons_count"] = 0
    if "last_comparison" not in st.session_state:
        st.session_state["last_comparison"] = None
    if "comparison_history" not in st.session_state:
        st.session_state["comparison_history"] = []
    if "canvas_height" not in st.session_state:
        st.session_state["canvas_height"] = 128
    if "canvas_width" not in st.session_state:
        st.session_state["canvas_width"] = 256
    if "margin_padding" not in st.session_state:
        st.session_state["margin_padding"] = 10
    if "similarity_threshold" not in st.session_state:
        st.session_state["similarity_threshold"] = 0.70
    if "ref_image_source" not in st.session_state:
        st.session_state["ref_image_source"] = None
    if "test_image_source" not in st.session_state:
        st.session_state["test_image_source"] = None
    if "ref_image_name" not in st.session_state:
        st.session_state["ref_image_name"] = "Reference Signature"
    if "test_image_name" not in st.session_state:
        st.session_state["test_image_name"] = "Test Signature"


def load_custom_css():
    """Injects custom product stylesheet into current page."""
    css_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "css", "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)


def render_header():
    """Renders clean, modern product header for SignatureLab."""
    init_session_state()
    load_custom_css()
    
    st.markdown(
        """
        <div class="app-header-container">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h1 class="app-title">
                        <span>✍️</span> <span class="app-title-highlight">SignatureLab</span> Studio
                    </h1>
                    <p class="app-subtitle">
                        High-Dimensional Vector Comparison & Preprocessing Engine
                    </p>
                </div>
                <div>
                    <span class="product-tag">
                        <span class="live-dot"></span> In-Memory Verification Engine
                    </span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_privacy_footer():
    """
    Renders privacy notice and prototype disclaimer.
    """
    st.markdown(
        """
        <div class="app-footer">
            <div style="font-weight: 600; color: #334155; margin-bottom: 6px;">
                SignatureLab — Handwritten Signature Comparison Tool
            </div>
            <div style="max-width: 780px; margin: 0 auto; color: #64748b; font-size: 0.82rem; line-height: 1.5;">
                <b>Privacy Notice:</b> Uploaded signature images are processed strictly in memory on this machine. 
                No files are sent to external servers or persisted to cloud storage.<br/>
                <b>Disclaimer:</b> This application provides numerical similarity metrics based on image stroke 
                preprocessing and vector geometry. It is a comparison prototype and does not provide legal, forensic, 
                or certified banking proof of biometric identity or authenticity.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Backwards compatibility alias
render_educational_footer = render_privacy_footer

