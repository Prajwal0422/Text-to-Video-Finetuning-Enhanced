"""
Input Validators
Validates user inputs and API requests
"""

import re
from typing import Dict, Optional

class PromptValidator:
    """Validates video generation prompts"""
    
    MIN_LENGTH = 3
    MAX_LENGTH = 500
    
    @staticmethod
    def validate(prompt: str) -> Dict[str, any]:
        """
        Validate prompt
        
        Returns:
            dict with 'valid' (bool) and 'error' (str) keys
        """
        if not prompt:
            return {'valid': False, 'error': 'Prompt is required'}
        
        if not isinstance(prompt, str):
            return {'valid': False, 'error': 'Prompt must be a string'}
        
        prompt = prompt.strip()
        
        if len(prompt) < PromptValidator.MIN_LENGTH:
            return {
                'valid': False,
                'error': f'Prompt too short (minimum {PromptValidator.MIN_LENGTH} characters)'
            }
        
        if len(prompt) > PromptValidator.MAX_LENGTH:
            return {
                'valid': False,
                'error': f'Prompt too long (maximum {PromptValidator.MAX_LENGTH} characters)'
            }
        
        # Check for malicious content
        if re.search(r'<script|javascript:|onerror=', prompt, re.IGNORECASE):
            return {'valid': False, 'error': 'Invalid characters in prompt'}
        
        return {'valid': True, 'error': None}
    
    @staticmethod
    def sanitize(prompt: str) -> str:
        """Sanitize prompt by removing special characters"""
        # Remove HTML tags
        prompt = re.sub(r'<[^>]+>', '', prompt)
        # Remove extra whitespace
        prompt = ' '.join(prompt.split())
        return prompt.strip()


class APIKeyValidator:
    """Validates API keys"""
    
    @staticmethod
    def validate_pexels_key(api_key: str) -> bool:
        """Validate Pexels API key format"""
        if not api_key:
            return False
        
        # Pexels keys are typically 56 characters
        if len(api_key) < 20:
            return False
        
        # Should be alphanumeric
        if not re.match(r'^[a-zA-Z0-9]+$', api_key):
            return False
        
        return True
