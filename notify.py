from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

def send_emergency_sms():
    """Sends SMS alert via Twilio when Geni detects emergency"""
    try:
        client = Client(os.getenv('TWILIO_SID'), os.getenv('TWILIO_TOKEN'))
        
        message = client.messages.create(
            body="🚨 GENI ALERT: Unresponsive person detected. Check camera feed immediately.",
            from_=os.getenv('TWILIO_NUMBER'),
            to=os.getenv('MY_PHONE')
        )
        
        print(f"✅ SMS sent successfully! SID: {message.sid}")
        return True
    except Exception as e:
        print(f"❌ SMS failed: {e}")
        return False