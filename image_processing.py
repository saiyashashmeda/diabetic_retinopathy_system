"""
UI animations and styling utilities for Streamlit.
"""

import streamlit as st
import time
from typing import Optional


def load_css():
    """
    Loads custom CSS styling for the application.
    """
    css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Header Styling */
    .app-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        animation: fadeInDown 0.6s ease-out;
    }

    .app-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }

    .app-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Card Styling */
    .custom-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
        border-left: 4px solid #1E88E5;
        animation: fadeIn 0.5s ease-out;
    }

    /* Upload Box */
    .upload-box {
        border: 3px dashed #1E88E5;
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        background: linear-gradient(145deg, #f8f9fa, #ffffff);
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .upload-box:hover {
        border-color: #43A047;
        transform: scale(1.02);
        box-shadow: 0 15px 30px rgba(30, 136, 229, 0.2);
    }

    /* Prediction Card */
    .prediction-card {
        background: white;
        border-left: 5px solid #43A047;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
        animation: slideInRight 0.5s ease-out;
    }

    /* Severity Badges */
    .severity-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }

    .severity-0 { background: #43A047; color: white; }
    .severity-1 { background: #FDD835; color: #333; }
    .severity-2 { background: #FB8C00; color: white; }
    .severity-3 { background: #F4511E; color: white; }
    .severity-4 { background: #E53935; color: white; }

    /* Report Sections */
    .report-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1E88E5;
        animation: fadeIn 0.5s ease-out;
    }

    .report-section h3 {
        color: #2C3E50;
        margin-top: 0;
        font-size: 1.3rem;
    }

    .report-section ul {
        margin: 0.5rem 0;
        padding-left: 1.5rem;
    }

    .report-section li {
        margin: 0.5rem 0;
        line-height: 1.6;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(102, 126, 234, 0.4);
    }

    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }

    .pulse {
        animation: pulse 2s infinite;
    }

    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }

    /* Info/Warning/Success boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        font-size: 1rem;
    }

    /* File Uploader */
    .stFileUploader {
        border: 2px dashed #1E88E5;
        border-radius: 10px;
        padding: 1rem;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1E88E5;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def show_header(title: str, subtitle: str, icon: str = "👁️"):
    """
    Displays an animated header.

    Args:
        title: Main title
        subtitle: Subtitle text
        icon: Icon emoji
    """
    st.markdown(f"""
        <div class="app-header">
            <h1>{icon} {title}</h1>
            <p>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def show_prediction_card(stage: str, confidence: float, stage_number: int):
    """
    Displays a prediction result card with animation.

    Args:
        stage: Predicted stage name
        confidence: Confidence score (0-1)
        stage_number: Stage number (0-4)
    """
    st.markdown(f"""
        <div class="prediction-card">
            <h3 style="color: #2C3E50; margin-top: 0;">
                Prediction Result
            </h3>
            <div class="severity-badge severity-{stage_number}">
                {stage}
            </div>
            <p style="font-size: 1.1rem; margin: 1rem 0 0 0;">
                Confidence: <strong>{confidence*100:.2f}%</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)


def show_loading_animation(message: str = "Processing..."):
    """
    Shows a loading animation with a message.

    Args:
        message: Loading message to display
    """
    with st.spinner(f"🔬 {message}"):
        time.sleep(0.5)  # Smooth UX


def show_success_message(message: str):
    """
    Shows an animated success message.

    Args:
        message: Success message
    """
    st.success(f"✅ {message}")
    st.balloons()


def show_error_message(message: str):
    """
    Shows an error message.

    Args:
        message: Error message
    """
    st.error(f"❌ {message}")


def show_warning_message(message: str):
    """
    Shows a warning message.

    Args:
        message: Warning message
    """
    st.warning(f"⚠️ {message}")


def show_info_message(message: str):
    """
    Shows an info message.

    Args:
        message: Info message
    """
    st.info(f"ℹ️ {message}")


def create_section_header(title: str, icon: str = "📋"):
    """
    Creates a styled section header.

    Args:
        title: Section title
        icon: Icon emoji
    """
    st.markdown(f"""
        <div style="margin: 2rem 0 1rem 0;">
            <h2 style="color: #2C3E50; border-bottom: 3px solid #1E88E5;
                       padding-bottom: 0.5rem; display: inline-block;">
                {icon} {title}
            </h2>
        </div>
    """, unsafe_allow_html=True)


def show_metric_card(label: str, value: str, delta: Optional[str] = None):
    """
    Shows a metric card with optional delta.

    Args:
        label: Metric label
        value: Metric value
        delta: Optional delta value
    """
    st.metric(label=label, value=value, delta=delta)


def add_vertical_space(lines: int = 1):
    """
    Adds vertical spacing.

    Args:
        lines: Number of line breaks
    """
    for _ in range(lines):
        st.write("")


def create_divider():
    """
    Creates a styled divider.
    """
    st.markdown("""
        <hr style="border: none; border-top: 2px solid #e0e0e0; margin: 2rem 0;">
    """, unsafe_allow_html=True)
