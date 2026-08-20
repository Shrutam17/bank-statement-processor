"""
LLM-based extraction for bank statements using GPT-4 Vision or Claude.
Provides format-agnostic extraction that works with any bank statement layout.
"""

import json
import base64
import io
from typing import Dict, List, Optional

from pdf2image import convert_from_path
from PIL import Image

from src.utils.config_loader import load_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LLMExtractor:
    """Extract transaction data from PDFs using LLM vision models"""
    
    def __init__(self, provider: Optional[str] = None):
        """
        Initialize LLM extractor
        
        Args:
            provider: LLM provider ('openai', 'anthropic', or None for config default)
        """
        config = load_config()
        self.config = config.get("extraction", {}).get("llm", {})
        self.provider = provider or self.config.get("provider", "anthropic")
        
        # Initialize the appropriate client
        self._init_client()
        
    def _init_client(self):
        """Initialize the LLM client based on provider"""
        import os
        
        if self.provider == "openai":
            try:
                from openai import OpenAI
                api_key = os.getenv(self.config.get("api_key_env", "OPENAI_API_KEY"))
                if not api_key:
                    raise ValueError(
                        f"API key not found in environment variable: "
                        f"{self.config.get('api_key_env', 'OPENAI_API_KEY')}"
                    )
                self.client = OpenAI(api_key=api_key)
                self.model = self.config.get("model", "gpt-4o")
                logger.info(f"Initialized OpenAI client with model: {self.model}")
            except ImportError:
                raise ImportError(
                    "OpenAI library not installed. Install with: pip install openai"
                )
                
        elif self.provider == "anthropic":
            try:
                import anthropic
                api_key = os.getenv(self.config.get("api_key_env", "ANTHROPIC_API_KEY"))
                if not api_key:
                    raise ValueError(
                        f"API key not found in environment variable: "
                        f"{self.config.get('api_key_env', 'ANTHROPIC_API_KEY')}"
                    )
                self.client = anthropic.Anthropic(api_key=api_key)
                self.model = self.config.get("model", "claude-3-5-sonnet-20241022")
                logger.info(f"Initialized Anthropic client with model: {self.model}")
            except ImportError:
                raise ImportError(
                    "Anthropic library not installed. Install with: pip install anthropic"
                )
                
        elif self.provider == "google":
            try:
                import google.generativeai as genai
                api_key = os.getenv(self.config.get("api_key_env", "GOOGLE_API_KEY"))
                if not api_key:
                    raise ValueError(
                        f"API key not found in environment variable: "
                        f"{self.config.get('api_key_env', 'GOOGLE_API_KEY')}"
                    )
                genai.configure(api_key=api_key)
                self.client = genai
                self.model = self.config.get("model", "gemini-1.5-flash")
                logger.info(f"Initialized Google Gemini client with model: {self.model}")
            except ImportError:
                raise ImportError(
                    "Google Generative AI library not installed. Install with: pip install google-generativeai"
                )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def extract(self, pdf_path: str) -> Dict:
        """
        Extract transactions and account details from a PDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with 'transactions' and 'account_details'
        """
        logger.info(f"Starting LLM extraction for: {pdf_path}")
        
        # Convert PDF to images
        images = self._pdf_to_images(pdf_path)
        logger.info(f"Converted PDF to {len(images)} images")
        
        # Extract from each page
        all_transactions = []
        account_details = None
        
        for page_num, image in enumerate(images, 1):
            logger.info(f"Processing page {page_num}/{len(images)} with LLM")
            
            page_data = self._extract_from_image(image, page_num)
            
            # Get account details from first page
            if page_num == 1 and page_data.get("account_details"):
                account_details = page_data["account_details"]
            
            # Collect transactions
            if page_data.get("transactions"):
                all_transactions.extend(page_data["transactions"])
        
        logger.info(
            f"LLM extraction complete: {len(all_transactions)} transactions found"
        )
        
        return {
            "transactions": all_transactions,
            "account_details": account_details or {},
        }
    
    def _pdf_to_images(self, pdf_path: str, dpi: int = 200) -> List[Image.Image]:
        """Convert PDF pages to images"""
        return convert_from_path(pdf_path, dpi=dpi)
    
    def _extract_from_image(self, image: Image.Image, page_num: int) -> Dict:
        """Extract data from a single page image using LLM"""
        
        if self.provider == "openai":
            return self._extract_openai(image, page_num)
        elif self.provider == "anthropic":
            return self._extract_anthropic(image, page_num)
        elif self.provider == "google":
            return self._extract_google(image, page_num)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def _extract_openai(self, image: Image.Image, page_num: int) -> Dict:
        """Extract using OpenAI GPT-4 Vision"""
        
        # Convert image to base64
        img_base64 = self._image_to_base64(image)
        
        # Create the extraction prompt
        prompt = self._create_extraction_prompt(page_num)
        
        try:
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
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=4096,
                temperature=0,  # Deterministic for extraction
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"OpenAI extraction failed: {e}")
            raise
    
    def _extract_anthropic(self, image: Image.Image, page_num: int) -> Dict:
        """Extract using Anthropic Claude"""
        
        # Convert image to base64
        img_base64 = self._image_to_base64(image)
        
        # Create the extraction prompt
        prompt = self._create_extraction_prompt(page_num)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": img_base64,
                                },
                            },
                            {"type": "text", "text": prompt},
                        ],
                    }
                ],
            )
            
            # Parse the JSON response
            content = response.content[0].text
            
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Anthropic extraction failed: {e}")
            raise
    
    def _extract_google(self, image: Image.Image, page_num: int) -> Dict:
        """Extract using Google Gemini"""
        
        # Create the extraction prompt
        prompt = self._create_extraction_prompt(page_num)
        
        try:
            # Initialize the model (ensure it has the models/ prefix)
            model_name = self.model if self.model.startswith("models/") else f"models/{self.model}"
            model = self.client.GenerativeModel(model_name)
            
            # Generate content with image and prompt
            response = model.generate_content(
                [prompt, image],
                generation_config={
                    "temperature": 0,  # Deterministic
                    "max_output_tokens": 4096,
                }
            )
            
            # Parse the JSON response
            content = response.text
            
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Google Gemini extraction failed: {e}")
            raise
    
    def _create_extraction_prompt(self, page_num: int) -> str:
        """Create the extraction prompt for the LLM"""
        
        account_details_instruction = """
    "account_details": {
        "account_holder_name": "Full Name Here",
        "account_number": "123456789",
        "ifsc_code": "ABCD0123456",
        "branch": "Branch Name"
    },""" if page_num == 1 else ""
        
        return f"""You are a bank statement parser. Extract ALL transactions and account details from this bank statement image.

Return ONLY valid JSON in this EXACT format (no additional text or markdown):

{{
    {account_details_instruction}
    "transactions": [
        {{
            "date": "DD/MM/YYYY",
            "description": "Transaction description",
            "debit": 0.00,
            "credit": 0.00,
            "balance": 0.00
        }}
    ]
}}

CRITICAL RULES:
1. Extract EVERY transaction visible in the image
2. For debit transactions (money out): set debit amount, credit = 0.00
3. For credit transactions (money in): set credit amount, debit = 0.00
4. Parse dates in DD/MM/YYYY format (or keep original format if different)
5. Remove commas from amounts: 1,000.00 → 1000.00
6. Keep descriptions exactly as shown
7. If account details not visible (page {page_num}), omit account_details section
8. Return ONLY the JSON object, no explanatory text

If the image shows no transactions (header page, footer, etc.), return:
{{"transactions": []}}"""
    
    def _image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        buffered = io.BytesIO()
        # Convert to RGB if necessary (handles transparency)
        if image.mode in ("RGBA", "LA", "P"):
            rgb_image = Image.new("RGB", image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
            image = rgb_image
        image.save(buffered, format="JPEG", quality=95)
        return base64.b64encode(buffered.getvalue()).decode()


class LLMExtractionError(Exception):
    """Raised when LLM extraction fails"""
    pass
