import africastalking
import os
from typing import List, Optional

class AfricaTalkingGateway:
    def __init__(self):
        self.username = os.getenv('AT_USERNAME')
        self.api_key = os.getenv('AT_API_KEY')
        self.sender_id = os.getenv('AT_SENDER_ID')
        self.initialized = False
        
        # Initialize Africa's Talking only if credentials are provided
        if self.username and self.api_key and self.username != 'sandbox':
            try:
                africastalking.initialize(self.username, self.api_key)
                self.initialized = True
            except Exception as e:
                print(f"Warning: Could not initialize Africa's Talking: {e}")
                print("Running in development mode without SMS/USSD capabilities")
        
        # Get service instances
        self.sms = africastalking.SMS
        self.voice = africastalking.Voice
        self.ussd = africastalking.USSD

    def send_sms(self, phone_numbers: List[str], message: str) -> dict:
        """Send SMS to one or more recipients"""
        try:
            response = self.sms.send(
                message,
                phone_numbers,
                self.sender_id
            )
            return {
                "status": "success",
                "message": "SMS sent successfully",
                "data": response
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def make_call(self, phone_number: str, callback_url: str) -> dict:
        """Initiate a voice call"""
        try:
            response = self.voice.call({
                'from': self.sender_id,
                'to': phone_number,
                'callbackUrl': callback_url
            })
            return {
                "status": "success",
                "message": "Call initiated successfully",
                "data": response
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def handle_ussd(self, session_id: str, phone_number: str, text: str) -> str:
        """Handle USSD session"""
        # This is a basic implementation. Extend based on your USSD menu flow
        if text == "":
            # First request
            response = "CON Welcome to AfyaSmart\n"
            response += "1. Find Hospital\n"
            response += "2. First Aid Help\n"
            response += "3. Emergency Contact"
            return response
            
        try:
            # Split user response into a list
            user_response = text.split('*')
            level = len(user_response)
            
            if level == 1:
                if text == "1":
                    response = "CON Select Zone:\n"
                    response += "1. Northern\n"
                    response += "2. Southern\n"
                    response += "3. Eastern\n"
                    response += "4. Western\n"
                    response += "5. Central"
                    return response
                    
                elif text == "2":
                    response = "CON Select condition:\n"
                    response += "1. Bleeding\n"
                    response += "2. Burns\n"
                    response += "3. Choking\n"
                    response += "4. Fracture"
                    return response
                    
                elif text == "3":
                    response = "END Emergency Contacts:\n"
                    response += "Police: 112\n"
                    response += "Ambulance: 114\n"
                    response += "Fire: 115"
                    return response
                    
            # Add more levels as needed
            
        except Exception as e:
            return f"END An error occurred: {str(e)}"
        
        return "END Invalid selection"

# Global instance
at_gateway = None

def init_at_gateway():
    """Initialize Africa's Talking Gateway"""
    global at_gateway
    at_gateway = AfricaTalkingGateway()

def get_at_gateway() -> AfricaTalkingGateway:
    """Get Africa's Talking Gateway instance"""
    if at_gateway is None:
        init_at_gateway()
    return at_gateway
