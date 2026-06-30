"""
Configuration file for Diabetic Retinopathy Detection System.
Loads settings from environment variables and defines constants.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "Saved Model" / "diabetic_retinopathy_model_complete.pth"
DATABASE_PATH = BASE_DIR / "database" / "users.db"
ASSETS_PATH = BASE_DIR / "assets"

# Model Configuration
CLASS_NAMES = [
    "No DR (Stage 0)",
    "Mild DR (Stage 1)",
    "Moderate DR (Stage 2)",
    "Severe DR (Stage 3)",
    "Proliferative DR (Stage 4)"
]

CLASS_DESCRIPTIONS = {
    0: "No Diabetic Retinopathy - Normal retinal health",
    1: "Mild DR - Early stage with minimal damage",
    2: "Moderate DR - Progressive damage requiring monitoring",
    3: "Severe DR - Advanced damage requiring treatment",
    4: "Proliferative DR - Critical stage requiring immediate intervention"
}

# Image preprocessing settings (from notebook analysis)
IMAGE_SIZE = (512, 512)  # Model was trained on 512x512 images
MEAN = [0.485, 0.456, 0.406]  # ImageNet normalization stats
STD = [0.229, 0.224, 0.225]

# Groq API Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-4-scout-17b-16e-instruct")  # Vision-capable model
GROQ_MODEL_FALLBACK = "llama-3.3-70b-versatile"  # Text-only backup
GROQ_TIMEOUT = 30  # API timeout in seconds
GROQ_MAX_TOKENS = 2048

# UI Configuration
APP_TITLE = "Diabetic Retinopathy Detection System"
APP_ICON = "👁️"
APP_SUBTITLE = "AI-Powered Retinal Image Analysis with Intelligent Reporting"
MAX_UPLOAD_SIZE = 10  # MB
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']

# Session Configuration
SESSION_TIMEOUT = 3600  # 1 hour in seconds
MIN_PASSWORD_LENGTH = 6

# Medical Report Configuration
REPORT_SECTIONS = [
    "executive_summary",
    "detailed_findings",
    "severity_analysis",
    "recommendations",
    "precautions",
    "follow_up",
    "lifestyle_modifications",
    "when_to_seek_help"
]

# Color Scheme (Medical Theme)
COLORS = {
    'primary': '#1E88E5',      # Medical Blue
    'secondary': '#43A047',     # Healthy Green
    'warning': '#FB8C00',       # Warning Orange
    'danger': '#E53935',        # Critical Red
    'background': '#F5F7FA',    # Light Gray
    'card_bg': '#FFFFFF',       # White
    'text_primary': '#2C3E50',  # Dark Blue-Gray
    'text_secondary': '#7F8C8D' # Medium Gray
}

# Severity Color Mapping
SEVERITY_COLORS = {
    0: COLORS['secondary'],  # Green for No DR
    1: '#FDD835',           # Yellow for Mild
    2: COLORS['warning'],   # Orange for Moderate
    3: '#F4511E',          # Deep Orange for Severe
    4: COLORS['danger']    # Red for Proliferative
}

# Database Configuration
DB_TABLES = {
    'users': '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''',
    'prediction_history': '''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            image_name TEXT,
            prediction_stage INTEGER,
            prediction_label TEXT,
            confidence REAL,
            report_generated BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    '''
}

# Validate configuration
def validate_config():
    """
    Validates that all required configurations are properly set.

    Returns:
        tuple: (is_valid, error_message)
    """
    if not GROQ_API_KEY:
        return False, "GROQ_API_KEY not found in environment variables. Please check your .env file."

    if not MODEL_PATH.exists():
        return False, f"Model file not found at {MODEL_PATH}"

    return True, "Configuration validated successfully"


# Export commonly used settings
__all__ = [
    'BASE_DIR', 'MODEL_PATH', 'DATABASE_PATH', 'CLASS_NAMES', 'IMAGE_SIZE',
    'MEAN', 'STD', 'GROQ_API_KEY', 'GROQ_MODEL', 'APP_TITLE', 'APP_ICON',
    'COLORS', 'SEVERITY_COLORS', 'validate_config'
]
