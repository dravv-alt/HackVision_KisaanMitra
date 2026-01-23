"""
Twilio Authentication Service
Handles OTP generation and verification using Twilio Verify V2 API
"""

import os
from typing import Dict
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

load_dotenv()

class TwilioAuthService:
    def __init__(self):
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.verify_sid = os.getenv("TWILIO_VERIFY_SERVICE_SID")
        
        # Initialize Twilio client
        if self.account_sid and self.auth_token and self.verify_sid:
            try:
                self.client = Client(self.account_sid, self.auth_token)
                self.enabled = True
            except Exception as e:
                print(f"⚠️ Twilio Client Init Error: {e}")
                self.client = None
                self.enabled = False
        else:
            self.client = None
            self.enabled = False
            print("⚠️ Twilio Verify credentials not configured. Using Mock OTP.")

    def send_otp(self, phone_number: str) -> Dict[str, any]:
        """
        Send OTP using Twilio Verify V2
        """
        if self.enabled:
            try:
                verification = self.client.verify.v2.services(
                    self.verify_sid
                ).verifications.create(to=phone_number, channel='sms')
                
                return {
                    "success": True,
                    "message": "OTP sent successfully via Twilio Verify",
                    "status": verification.status,
                    "expires_in_minutes": 10
                }
            except TwilioRestException as e:
                return {
                    "success": False,
                    "message": f"Twilio Error: {e.msg}"
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"System Error: {str(e)}"
                }
        else:
            # Mock Mode
            return {
                "success": True,
                "message": "OTP sent (Mock Mode)",
                "otp": "123456",
                "expires_in_minutes": 10
            }

    def verify_otp(self, phone_number: str, otp: str) -> Dict[str, any]:
        """
        Verify OTP using Twilio Verify V2
        """
        if self.enabled:
            try:
                verification_check = self.client.verify.v2.services(
                    self.verify_sid
                ).verification_checks.create(to=phone_number, code=otp)

                if verification_check.status == "approved":
                    return {
                        "success": True,
                        "message": "OTP Verified Successfully",
                        "phone_number": phone_number
                    }
                else:
                    return {
                        "success": False,
                        "message": "Invalid OTP or Expired"
                    }
            except TwilioRestException as e:
                return {
                    "success": False,
                    "message": f"Twilio Verification Error: {e.msg}"
                }
            except Exception as e:
                return {
                    "success": False,
                    "message": f"Verification Failed: {str(e)}"
                }
        else:
            # Mock Mode
            if otp == "123456":
                return {
                    "success": True,
                    "message": "OTP Verified (Mock)",
                    "phone_number": phone_number
                }
            return {
                "success": False,
                "message": "Invalid Mock OTP"
            }

    def resend_otp(self, phone_number: str) -> Dict[str, any]:
        return self.send_otp(phone_number)

# Singleton instance
_twilio_service = None

def get_twilio_service() -> TwilioAuthService:
    """Get singleton instance of TwilioAuthService"""
    global _twilio_service
    if _twilio_service is None:
        _twilio_service = TwilioAuthService()
    return _twilio_service
