import smtplib
from twilio.rest import Client

EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"
EMAIL_RECEIVER = "receiver_email@gmail.com"

TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE = "+1234567890"
RECIPIENT_PHONE = "+0987654321"

def send_email_alert(threat_message):
"""Send email alert."""
try:
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL_SENDER, EMAIL_PASSWORD)
message = f"Subject: 🚨 THREAT ALERT 🚨\n\n{threat_message}"
server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, message)
server.quit()
print("📧 Email alert sent!")
except Exception as e:
print(f"Email error: {e}")

def send_sms_alert(threat_message):
"""Send SMS alert via Twilio."""
try:
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
message = client.messages.create(
body=threat_message,
from_=TWILIO_PHONE,
to=RECIPIENT_PHONE
)
print("📱 SMS alert sent!")
except Exception as e:
print(f"SMS error: {e}")
