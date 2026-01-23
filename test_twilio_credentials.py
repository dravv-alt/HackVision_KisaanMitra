
import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv('Backend/.env')

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone = os.getenv("TWILIO_PHONE_NUMBER")

print(f"Account SID: {account_sid}")
# Mask token for security in logs
masked_token = auth_token[:4] + "***" + auth_token[-4:] if auth_token else "None"
print(f"Auth Token: {masked_token}")
print(f"From Phone: {twilio_phone}")

if not account_sid or not auth_token:
    print("❌ Missing Twilio credentials")
    exit(1)

try:
    client = Client(account_sid, auth_token)
    # Fetch account details to verify credentials
    account = client.api.accounts(account_sid).fetch()
    print(f"✅ Credentials Valid! Account Name: {account.friendly_name}")
    print(f"✅ Status: {account.status}")
    print(f"✅ Type: {account.type}")
except Exception as e:
    print(f"❌ Credentials Invalid or Network Error: {str(e)}")
