# Diabetic Retinopathy Detection System

AI-powered retinal image analysis system with intelligent medical report generation using deep learning and large language models.

## Features

- **5-Stage Classification**: Detects diabetic retinopathy from No DR to Proliferative DR
- **Deep Learning**: ResNet34 model trained on retinal fundus images
- **AI-Powered Reports**: Comprehensive medical reports generated using Groq LLM
- **Secure Authentication**: User registration and login with bcrypt password hashing
- **Prediction History**: Track and review past predictions
- **Professional UI**: Clean, medical-themed interface with animations
- **Downloadable Reports**: Export detailed medical reports

## Technology Stack

### Frontend
- **Streamlit**: Interactive web application framework
- **Custom CSS**: Professional medical-themed styling

### Backend
- **Python 3.8+**: Core programming language
- **PyTorch**: Deep learning framework
- **torchvision**: Pre-trained models and image transformations

### AI/ML
- **ResNet34**: Pre-trained CNN model for image classification
- **Groq API**: LLM-powered medical report generation (Llama 4 Scout)

### Database
- **SQLite3**: User authentication and prediction history

### Security
- **bcrypt**: Password hashing
- **python-dotenv**: Environment variable management

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Diabetic_Resnet_Agentic
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # Linux/Mac
   ```

2. Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

   Get your free API key from: https://console.groq.com/keys

### Step 5: Verify Model File

Ensure the trained model file exists at:
```
Saved Model/diabetic_retinopathy_model_complete.pth
```

## Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Usage Guide

### 1. Registration

1. Open the application
2. Click on the "Register" tab
3. Fill in your details:
   - Full Name
   - Username
   - Password (minimum 6 characters)
   - Confirm Password
4. Accept the terms and conditions
5. Click "Create Account"

### 2. Login

1. Click on the "Login" tab
2. Enter your username and password
3. Click "Login"

### 3. Upload Image

1. After logging in, click "Browse files"
2. Select a retinal fundus image (JPG, PNG, or JPEG)
3. The image will be displayed for verification

### 4. Get Prediction

1. Click "Predict Stage"
2. The AI will analyze the image
3. View the prediction result and confidence score
4. See probability distribution across all stages

### 5. Generate Report

1. After prediction, click "Generate Detailed Medical Report"
2. Wait for the AI to generate a comprehensive report
3. Review the following sections:
   - Executive Summary
   - Detailed Findings
   - Severity Analysis
   - Recommendations
   - Precautions
   - Follow-up Schedule
   - Lifestyle Modifications
   - Warning Signs

### 6. Download Report

- Click "Download Report (TXT)" to save the report
- Reports are formatted for easy reading and sharing

## Project Structure

```
Diabetic_Resnet_Agentic/
│
├── app.py                      # Main application entry point
├── config.py                   # Configuration and constants
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (not in git)
├── .env.example                # Environment template
├── README.md                   # This file
│
├── auth/                       # Authentication module
│   ├── __init__.py
│   ├── database.py             # Database manager
│   ├── auth_manager.py         # Authentication logic
│   └── hash_utils.py           # Password hashing
│
├── model/                      # AI/ML module
│   ├── __init__.py
│   ├── predictor.py            # Model loading and prediction
│   └── report_generator.py    # LLM-based report generation
│
├── ui/                         # User interface module
│   ├── __init__.py
│   ├── login_page.py           # Login/register page
│   ├── upload_page.py          # Image upload and prediction
│   └── report_page.py          # Report display
│
├── utils/                      # Utilities module
│   ├── __init__.py
│   ├── image_processing.py    # Image preprocessing
│   └── animations.py           # UI styling and animations
│
├── database/                   # SQLite database (auto-created)
│   └── users.db
│
├── Saved Model/                # Trained model
│   └── diabetic_retinopathy_model_complete.pth
│
└── Notebook/                   # Training notebook
    └── diabetic-retinopathy-detection-using-resnet34.ipynb
```

## Model Details

### Architecture

- **Base Model**: ResNet34 (pre-trained on ImageNet)
- **Custom Layers**:
  - Linear(512 → 256)
  - Linear(256 → 128)
  - Linear(128 → 64)
  - Linear(64 → 5)

### Input Specifications

- **Image Size**: 512×512 pixels
- **Color Space**: RGB
- **Normalization**: ImageNet statistics
  - Mean: [0.485, 0.456, 0.406]
  - Std: [0.229, 0.224, 0.225]

### Output Classes

0. **No DR (Stage 0)**: No diabetic retinopathy detected
1. **Mild DR (Stage 1)**: Early stage with minimal damage
2. **Moderate DR (Stage 2)**: Progressive damage requiring monitoring
3. **Severe DR (Stage 3)**: Advanced damage requiring treatment
4. **Proliferative DR (Stage 4)**: Critical stage requiring immediate intervention

## API Configuration

The system uses Groq's LLM API for report generation.

### Models Used

1. **Primary**: `llama-4-scout-17b-16e-instruct` (vision-capable)
2. **Fallback**: `llama-3.3-70b-versatile` (text-only)

### Rate Limits

- Groq free tier: Check https://console.groq.com for current limits
- Fallback to text-only model if vision model fails

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);
```

### Prediction History Table

```sql
CREATE TABLE prediction_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    image_name TEXT,
    prediction_stage INTEGER,
    prediction_label TEXT,
    confidence REAL,
    report_generated BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Security Considerations

### Password Security

- Passwords hashed using bcrypt with 12 salt rounds
- Plain-text passwords never stored
- Minimum password length: 6 characters

### API Key Security

- Stored in `.env` file (not committed to git)
- Loaded using python-dotenv
- Never exposed in code or logs

### Session Management

- Session state managed by Streamlit
- User data cleared on logout
- No persistent sessions across browser closes

## Troubleshooting

### Model Loading Error

**Error**: `Model file not found`

**Solution**: Ensure the `.pth` file exists in `Saved Model/` directory

### API Key Error

**Error**: `Groq API key not found`

**Solution**:
1. Check `.env` file exists
2. Verify `GROQ_API_KEY` is set correctly
3. Restart the application

### Database Error

**Error**: `Database connection failed`

**Solution**:
1. Ensure `database/` directory has write permissions
2. Delete `users.db` and restart (WARNING: loses data)

### Import Error

**Error**: `Module not found`

**Solution**:
```bash
pip install -r requirements.txt
```

## Disclaimer

**IMPORTANT**: This system is a research tool and should **NOT** replace professional medical diagnosis.

- Results are for informational purposes only
- Always consult a qualified ophthalmologist for proper medical evaluation
- Do not make treatment decisions based solely on this system
- The AI may make errors or provide incomplete information

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and research purposes.

## Support

For issues, questions, or suggestions:
- Create an issue on GitHub
- Contact the development team

## Acknowledgments

- **Dataset**: APTOS 2019 Blindness Detection Challenge
- **Model**: PyTorch and torchvision teams
- **LLM**: Groq for providing API access
- **Framework**: Streamlit for the excellent web framework

## Version History

### v1.0.0 (Current)
- Initial release
- ResNet34 classification
- Groq LLM report generation
- User authentication
- Prediction history

## Future Enhancements

- [ ] Multi-language support
- [ ] PDF report export
- [ ] Email report delivery
- [ ] Prediction history dashboard
- [ ] Comparative analysis over time
- [ ] Admin panel
- [ ] Dark mode
- [ ] Mobile responsive design
- [ ] Integration with EHR systems

---

**Built with ❤️ using Python, PyTorch, and Streamlit**
