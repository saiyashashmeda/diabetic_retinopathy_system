"""
Model predictor for diabetic retinopathy detection.
Handles model loading and prediction.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models
from PIL import Image
from typing import Dict, Any, Optional
import config
from utils.image_processing import preprocess_image, load_image_from_upload, load_image_from_file
import streamlit as st


class DiabeticRetinopathyPredictor:
    """
    Predictor class for diabetic retinopathy detection using ResNet34.
    """

    def __init__(self, model_path: Optional[str] = None):
        """
        Initializes the predictor and loads the model.

        Args:
            model_path: Path to model file. If None, uses path from config.
        """
        self.model_path = model_path or config.MODEL_PATH
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None
        self.model_info = None
        self._load_model()

    def _create_model_architecture(self) -> nn.Module:
        """
        Creates the ResNet34 model architecture with custom FC layer.

        Returns:
            PyTorch model

        Note:
            Architecture from notebook:
            - ResNet34 base (pre-trained on ImageNet)
            - Custom FC: Linear(512→256) → Linear(256→128) → Linear(128→64) → Linear(64→5)
        """
        # Load pre-trained ResNet34
        model = models.resnet34(pretrained=False)  # We'll load our trained weights

        # Replace the final fully connected layer with custom layers
        model.fc = nn.Sequential(
            nn.Linear(512, 256),
            nn.Linear(256, 128),
            nn.Linear(128, 64),
            nn.Linear(64, 5)  # 5 classes
        )

        return model

    def _load_model(self):
        """
        Loads the trained model from the .pth file.

        Raises:
            FileNotFoundError: If model file doesn't exist
            Exception: If model loading fails
        """
        try:
            # Check if model file exists
            if not self.model_path.exists():
                raise FileNotFoundError(f"Model file not found at {self.model_path}")

            # Load model info
            self.model_info = torch.load(
                self.model_path,
                map_location=self.device,
                weights_only=False
            )

            # Create model architecture
            self.model = self._create_model_architecture()

            # Load trained weights
            self.model.load_state_dict(self.model_info['model_state_dict'])

            # Move model to device
            self.model = self.model.to(self.device)

            # Set model to evaluation mode
            self.model.eval()

            print(f"✓ Model loaded successfully on {self.device}")
            print(f"  Architecture: {self.model_info.get('model_architecture', 'resnet34')}")
            print(f"  Classes: {self.model_info.get('num_classes', 5)}")
            print(f"  Image Size: {self.model_info.get('image_size', 512)}x{self.model_info.get('image_size', 512)}")

        except FileNotFoundError as e:
            raise FileNotFoundError(str(e))
        except Exception as e:
            raise Exception(f"Failed to load model: {str(e)}")

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """
        Predicts diabetic retinopathy stage from a retinal image.

        Args:
            image: PIL Image object

        Returns:
            Dictionary containing:
                - stage: Stage name (e.g., "Moderate DR (Stage 2)")
                - stage_number: Stage number (0-4)
                - confidence: Confidence score (0.0-1.0)
                - all_probabilities: Dict of all class probabilities

        Example:
            >>> predictor = DiabeticRetinopathyPredictor()
            >>> image = Image.open("retina.jpg")
            >>> result = predictor.predict(image)
            >>> print(f"Prediction: {result['stage']}")
            >>> print(f"Confidence: {result['confidence']:.2%}")
        """
        if self.model is None:
            raise Exception("Model not loaded. Please initialize the predictor first.")

        try:
            # Preprocess image
            image_tensor = preprocess_image(image)
            image_tensor = image_tensor.to(self.device)

            # Make prediction
            with torch.no_grad():
                output = self.model(image_tensor)
                probabilities = F.softmax(output, dim=1)

            # Get prediction
            prob_values = probabilities.cpu().numpy()[0]
            predicted_class = int(prob_values.argmax())
            confidence = float(prob_values[predicted_class])

            # Create probability dictionary
            all_probabilities = {
                config.CLASS_NAMES[i]: float(prob_values[i])
                for i in range(len(config.CLASS_NAMES))
            }

            return {
                'stage': config.CLASS_NAMES[predicted_class],
                'stage_number': predicted_class,
                'confidence': confidence,
                'all_probabilities': all_probabilities,
                'description': config.CLASS_DESCRIPTIONS[predicted_class]
            }

        except Exception as e:
            raise Exception(f"Prediction failed: {str(e)}")

    def predict_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Predicts diabetic retinopathy stage from an image file.

        Args:
            file_path: Path to image file

        Returns:
            Prediction dictionary (same as predict method)
        """
        image = load_image_from_file(file_path)
        return self.predict(image)

    def predict_from_upload(self, uploaded_file) -> Dict[str, Any]:
        """
        Predicts diabetic retinopathy stage from a Streamlit uploaded file.

        Args:
            uploaded_file: Streamlit UploadedFile object

        Returns:
            Prediction dictionary (same as predict method)
        """
        image = load_image_from_upload(uploaded_file)
        return self.predict(image)

    def get_model_info(self) -> Dict[str, Any]:
        """
        Returns information about the loaded model.

        Returns:
            Dictionary with model information
        """
        return {
            'architecture': self.model_info.get('model_architecture', 'resnet34'),
            'num_classes': self.model_info.get('num_classes', 5),
            'image_size': self.model_info.get('image_size', 512),
            'device': str(self.device),
            'class_names': config.CLASS_NAMES
        }


# Cached predictor instance for Streamlit
@st.cache_resource
def get_predictor() -> DiabeticRetinopathyPredictor:
    """
    Returns a cached instance of the predictor (for Streamlit).

    Returns:
        DiabeticRetinopathyPredictor instance

    Note:
        Uses @st.cache_resource to load the model only once per session.
    """
    return DiabeticRetinopathyPredictor()


# Singleton instance (non-Streamlit usage)
_predictor = None


def get_predictor_instance() -> DiabeticRetinopathyPredictor:
    """
    Returns singleton instance of the predictor (for non-Streamlit usage).

    Returns:
        DiabeticRetinopathyPredictor instance
    """
    global _predictor
    if _predictor is None:
        _predictor = DiabeticRetinopathyPredictor()
    return _predictor
