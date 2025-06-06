import os
import aiohttp
import logging
from typing import Dict, Optional

class AIService:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.api_url = os.getenv('OPENROUTER_API_URL')
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'HTTP-Referer': 'https://afyasmart.com',
            'Content-Type': 'application/json'
        }
        
        # Define Rafiki's system prompt
        self.SYSTEM_PROMPT = """
        You are Rafiki, a knowledgeable health assistant focused on healthcare in Tanzania. 
        You provide concise, clear advice about health issues and information about hospitals 
        and health centers in Tanzania and their addresses (region, district, zone). Keep your responses brief, practical, and culturally 
        appropriate for Tanzanian users. Only answer health-related questions and hospital 
        information queries. For all other topics, politely explain that you can only help 
        with health matters.
        """
        
        # Define specific prompts
        self.FIRST_AID_PROMPT = """
        Provide brief, clear first aid steps for: {condition}
        Focus only on immediate actions before professional help arrives.
        List steps in order of priority.
        End with when to seek immediate medical care.
        Keep it very concise.
        """
        
        self.GENERAL_HEALTH_PROMPT = """
        Provide brief, clear advice about: {query}
        Focus on practical information relevant to Tanzania.
        Include when to see a healthcare provider.
        Keep it very concise.
        """

    async def _get_ai_response(self, messages: list) -> str:
        """Get response from OpenRouter API"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_url,
                headers=self.headers,
                json={
                    'model': 'anthropic/claude-3-opus',
                    'messages': messages,
                    'temperature': 0.7,
                    'max_tokens': 300
                }
            ) as response:
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' in content_type:
                    try:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    except Exception as e:
                        logging.exception("Failed to parse JSON from OpenRouter response")
                        raise Exception("AI service returned invalid data. Please try again later.")
                else:
                    text = await response.text()
                    logging.error(f"OpenRouter returned non-JSON response: {text}")
                    raise Exception("AI service is temporarily unavailable. Please try again later.")

    async def get_first_aid_guidance(self, condition: str, language: str = 'en') -> Dict:
        """Get first aid guidance for a specific condition"""
        try:
            prompt = self.FIRST_AID_PROMPT.format(condition=condition)
            messages = [
                {'role': 'system', 'content': self.SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt + (' (Please respond in Swahili)' if language == 'sw' else '')}
            ]
            
            response = await self._get_ai_response(messages)
            
            return {
                "status": "success",
                "message": "First aid guidance generated successfully",
                "data": {
                    "condition": condition,
                    "guidance": response
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating first aid guidance: {str(e)}"
            }

    async def get_health_advice(self, query: str, language: str = 'en') -> Dict:
        """Get general health advice"""
        try:
            prompt = self.GENERAL_HEALTH_PROMPT.format(query=query)
            messages = [
                {'role': 'system', 'content': self.SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt + (' (Please respond in Swahili)' if language == 'sw' else '')}
            ]
            
            response = await self._get_ai_response(messages)
            
            return {
                "status": "success",
                "message": "Health advice generated successfully",
                "data": {
                    "query": query,
                    "advice": response
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error generating health advice: {str(e)}"
            }

# Global instance
ai_service = None

def init_ai_service():
    """Initialize AI Service"""
    global ai_service
    ai_service = AIService()

def get_ai_service() -> AIService:
    """Get AI Service instance"""
    if ai_service is None:
        init_ai_service()
    return ai_service
