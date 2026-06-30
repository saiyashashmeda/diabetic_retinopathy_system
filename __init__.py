"""
AI-powered medical report generator using Groq LLM API.
Generates comprehensive medical reports for diabetic retinopathy predictions.
"""

from groq import Groq
from PIL import Image
import base64
import io
from typing import Dict, Any, Optional
import config
import json


class MedicalReportGenerator:
    """
    Generates detailed medical reports using Groq's LLM API.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the report generator.

        Args:
            api_key: Groq API key. If None, uses key from config.

        Raises:
            ValueError: If API key is not provided
        """
        self.api_key = api_key or config.GROQ_API_KEY

        if not self.api_key:
            raise ValueError("Groq API key not found. Please set GROQ_API_KEY in .env file.")

        self.client = Groq(api_key=self.api_key)
        self.model = config.GROQ_MODEL
        self.fallback_model = config.GROQ_MODEL_FALLBACK

    def _image_to_base64(self, image: Image.Image) -> str:
        """
        Converts PIL Image to base64 string.

        Args:
            image: PIL Image object

        Returns:
            Base64 encoded image string
        """
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')

    def _create_prompt(self, prediction_result: Dict[str, Any]) -> str:
        """
        Creates a detailed prompt for the LLM based on prediction results.

        Args:
            prediction_result: Dictionary from predictor containing stage, confidence, etc.

        Returns:
            Formatted prompt string
        """
        stage = prediction_result['stage']
        stage_number = prediction_result['stage_number']
        confidence = prediction_result['confidence']
        all_probs = prediction_result['all_probabilities']

        # Format probability distribution
        prob_str = "\n".join([
            f"  - {name}: {prob*100:.2f}%"
            for name, prob in all_probs.items()
        ])

        prompt = f"""You are an expert ophthalmologist specializing in diabetic retinopathy diagnosis.
Analyze the provided retinal image and AI prediction results to generate a comprehensive, professional medical report.

**AI PREDICTION RESULTS:**
- Detected Stage: {stage}
- Stage Number: {stage_number} (0=Normal, 1=Mild, 2=Moderate, 3=Severe, 4=Proliferative)
- Confidence: {confidence*100:.2f}%

**Probability Distribution:**
{prob_str}

**TASK:**
Generate a detailed medical report with the following sections. Format your response as a JSON object with these exact keys:

1. **executive_summary**: A 2-3 sentence overview of the findings (string)

2. **detailed_findings**: Detailed description of retinal features visible in the image. Describe what pathological changes would typically be present at this stage, such as:
   - Microaneurysms
   - Hemorrhages
   - Hard exudates
   - Cotton wool spots
   - Neovascularization (if applicable)
   - Macular edema (if applicable)
   (Provide a paragraph of at least 4-5 sentences)

3. **severity_analysis**: Explain the clinical significance of this stage, progression risk, and impact on vision. Include information about how this stage compares to others and what it means for the patient's prognosis. (Provide a detailed paragraph)

4. **recommendations**: Array of at least 5 specific, actionable recommendations. Examples:
   - Medical examinations needed
   - Specialist referrals
   - Treatment options
   - Medication reviews
   - Monitoring schedules
   (Return as array of strings)

5. **precautions**: Array of at least 5 medical and lifestyle precautions. Include:
   - Blood sugar management guidelines
   - Blood pressure control
   - Dietary recommendations
   - Activities to avoid
   - Eye care practices
   (Return as array of strings)

6. **follow_up**: Specific timeline and schedule for next examination and re-evaluation. Be very specific about when to return. (String with clear timeline)

7. **lifestyle_modifications**: Array of at least 5 evidence-based lifestyle changes that can help:
   - Diet modifications
   - Exercise recommendations
   - Sleep and stress management
   - Smoking/alcohol guidelines
   - Supplement recommendations
   (Return as array of strings)

8. **when_to_seek_help**: Array of at least 5 warning signs and symptoms that require immediate medical attention:
   - Vision changes
   - Pain indicators
   - Other red flags
   (Return as array of strings)

**IMPORTANT FORMATTING INSTRUCTIONS:**
- Return ONLY a valid JSON object with the 8 keys above
- Use double quotes for all strings
- Arrays should contain strings only
- Do NOT include any markdown, code blocks, or extra text outside the JSON
- Make the tone professional yet empathetic
- Avoid excessive medical jargon - explain terms when used
- Be specific and actionable in recommendations

Return the report as a properly formatted JSON object now:"""

        return prompt

    def generate_report_with_image(
        self,
        image: Image.Image,
        prediction_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates medical report using vision-capable model (with image).

        Args:
            image: PIL Image object of retinal scan
            prediction_result: Prediction dictionary from predictor

        Returns:
            Dictionary with report sections

        Raises:
            Exception: If API call fails
        """
        try:
            # Convert image to base64
            image_base64 = self._image_to_base64(image)

            # Create prompt
            prompt = self._create_prompt(prediction_result)

            # Call Groq API with vision model
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.7,
                max_tokens=config.GROQ_MAX_TOKENS,
                timeout=config.GROQ_TIMEOUT
            )

            # Extract response
            report_text = response.choices[0].message.content

            # Parse JSON response
            report = self._parse_report_response(report_text)

            return report

        except Exception as e:
            print(f"Vision model failed: {str(e)}")
            print("Falling back to text-only model...")
            return self.generate_report_text_only(prediction_result)

    def generate_report_text_only(
        self,
        prediction_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates medical report using text-only model (fallback).

        Args:
            prediction_result: Prediction dictionary from predictor

        Returns:
            Dictionary with report sections

        Raises:
            Exception: If API call fails
        """
        try:
            # Create prompt (same as vision model)
            prompt = self._create_prompt(prediction_result)

            # Call Groq API with text-only model
            response = self.client.chat.completions.create(
                model=self.fallback_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ophthalmologist specializing in diabetic retinopathy. Generate detailed medical reports based on AI predictions."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=config.GROQ_MAX_TOKENS,
                timeout=config.GROQ_TIMEOUT
            )

            # Extract response
            report_text = response.choices[0].message.content

            # Parse JSON response
            report = self._parse_report_response(report_text)

            return report

        except Exception as e:
            raise Exception(f"Report generation failed: {str(e)}")

    def _parse_report_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parses the LLM response into structured report dictionary.

        Args:
            response_text: Raw response from LLM

        Returns:
            Structured report dictionary

        Raises:
            ValueError: If response cannot be parsed
        """
        try:
            # Try to extract JSON from response
            # Remove markdown code blocks if present
            text = response_text.strip()

            if text.startswith("```json"):
                text = text[7:]
            elif text.startswith("```"):
                text = text[3:]

            if text.endswith("```"):
                text = text[:-3]

            text = text.strip()

            # Parse JSON
            report = json.loads(text)

            # Validate required keys
            required_keys = [
                'executive_summary',
                'detailed_findings',
                'severity_analysis',
                'recommendations',
                'precautions',
                'follow_up',
                'lifestyle_modifications',
                'when_to_seek_help'
            ]

            for key in required_keys:
                if key not in report:
                    raise ValueError(f"Missing required key: {key}")

            return report

        except json.JSONDecodeError as e:
            # If JSON parsing fails, create a basic report from the text
            print(f"JSON parsing failed: {str(e)}")
            print("Creating fallback report structure...")
            return self._create_fallback_report(response_text)

    def _create_fallback_report(self, text: str) -> Dict[str, Any]:
        """
        Creates a basic report structure if JSON parsing fails.

        Args:
            text: Raw LLM response text

        Returns:
            Basic report dictionary
        """
        return {
            'executive_summary': text[:500] if len(text) > 500 else text,
            'detailed_findings': "Please consult the full report text below.",
            'severity_analysis': "Analysis included in full report.",
            'recommendations': [
                "Consult with a qualified ophthalmologist",
                "Schedule a comprehensive eye examination",
                "Maintain strict blood sugar control",
                "Monitor blood pressure regularly",
                "Follow up as recommended by your doctor"
            ],
            'precautions': [
                "Control blood glucose levels",
                "Maintain healthy blood pressure",
                "Follow a balanced diet",
                "Exercise regularly",
                "Avoid smoking and limit alcohol"
            ],
            'follow_up': "Please schedule a follow-up appointment with your ophthalmologist within 3-6 months.",
            'lifestyle_modifications': [
                "Adopt a diabetes-friendly diet",
                "Engage in regular physical activity",
                "Maintain healthy sleep patterns",
                "Manage stress effectively",
                "Take medications as prescribed"
            ],
            'when_to_seek_help': [
                "Sudden vision loss or changes",
                "Persistent eye pain",
                "Seeing flashes or floaters",
                "Blurred vision that doesn't improve",
                "Any new visual disturbances"
            ],
            'full_text': text
        }

    def generate_report(
        self,
        prediction_result: Dict[str, Any],
        image: Optional[Image.Image] = None
    ) -> Dict[str, Any]:
        """
        Main method to generate medical report.

        Args:
            prediction_result: Prediction dictionary from predictor
            image: Optional PIL Image (will use vision model if provided)

        Returns:
            Dictionary with report sections
        """
        if image is not None:
            # Try vision model first
            return self.generate_report_with_image(image, prediction_result)
        else:
            # Use text-only model
            return self.generate_report_text_only(prediction_result)


# Singleton instance
_report_generator = None


def get_report_generator() -> MedicalReportGenerator:
    """
    Returns singleton instance of MedicalReportGenerator.

    Returns:
        MedicalReportGenerator instance
    """
    global _report_generator
    if _report_generator is None:
        _report_generator = MedicalReportGenerator()
    return _report_generator
