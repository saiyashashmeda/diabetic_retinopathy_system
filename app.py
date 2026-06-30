"""
Main application file for Diabetic Retinopathy Detection System.
Entry point for the Streamlit application.
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import config
from ui.login_page import show_login_page
from ui.upload_page import show_upload_page
from ui.report_page import show_report_page


# Page configuration (must be first Streamlit command)
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': f"""
        # {config.APP_TITLE}

        AI-powered diabetic retinopathy detection system with intelligent medical reporting.

        **Features:**
        - 5-stage diabetic retinopathy classification
        - ResNet34 deep learning model
        - AI-generated medical reports using Groq LLM
        - Secure user authentication
        - Prediction history tracking

        **Technology Stack:**
        - Frontend: Streamlit
        - Backend: Python, PyTorch
        - LLM: Groq API (Llama 4 Scout)
        - Database: SQLite3

        **Version:** 1.0.0
        """
    }
)


def initialize_session_state():
    """
    Initializes session state variables.
    """
    # Authentication
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if 'user' not in st.session_state:
        st.session_state.user = None

    # Prediction and report
    if 'prediction' not in st.session_state:
        st.session_state.prediction = None

    if 'report' not in st.session_state:
        st.session_state.report = None

    # Uploaded image
    if 'uploaded_image' not in st.session_state:
        st.session_state.uploaded_image = None

    if 'uploaded_filename' not in st.session_state:
        st.session_state.uploaded_filename = None


def validate_configuration():
    """
    Validates that the application is properly configured.
    """
    # Validate config
    is_valid, message = config.validate_config()

    if not is_valid:
        st.error(f"❌ Configuration Error: {message}")
        st.stop()


def main():
    """
    Main application logic.
    """
    # Initialize session state
    initialize_session_state()

    # Validate configuration
    validate_configuration()

    # Route based on authentication and state
    if not st.session_state.logged_in:
        # Show login/register page
        show_login_page()

    else:
        # User is logged in
        if st.session_state.report is not None:
            # Show report page
            show_report_page()

        else:
            # Show upload and analysis page
            show_upload_page()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"""
            ❌ **Application Error**

            An unexpected error occurred:
            ```
            {str(e)}
            ```

            Please refresh the page or contact support if the issue persists.
        """)

        # Show error details in expander
        with st.expander("Technical Details"):
            import traceback
            st.code(traceback.format_exc())
