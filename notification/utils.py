from twilio.rest import Client
from django.conf import settings

def format_phone_number(phone, country="IN"):
    """
    Format a phone number by adding the default country code if missing.
    
    Parameters:
    - phone (str): The raw phone number.
    - country (str): The default country code (e.g., "IN" for India).
    
    Returns:
    - str: The formatted phone number in E.164 format.
    """
    if not phone.startswith("+"):
        phone = f"+91{phone}"  # Add default country code for India
    return phone

def send_notification_sms(donor, recipient):
    """
    Send SMS notifications to the donor and recipient about the organ match.
    """
    from twilio.rest import Client
    from django.conf import settings

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Format phone numbers
    donor_phone = format_phone_number(donor['phone'])
    recipient_phone = format_phone_number(recipient['phone'])

    donor_message = (
        f"Hello {donor['name']},\n\n"
        f"A recipient has been found for your donation of {donor['organ']}."
    )
    recipient_message = (
        f"Hello {recipient['name']},\n\n"
        f"A donor has been found for the organ you need: {recipient['organ_required']}."
    )

    try:
        # Send SMS to donor
        print(f"Sending SMS to donor {donor['name']} at {donor_phone}")
        client.messages.create(
            body=donor_message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=donor_phone
        )

        # Send SMS to recipient
        print(f"Sending SMS to recipient {recipient['name']} at {recipient_phone}")
        client.messages.create(
            body=recipient_message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=recipient_phone
        )
    except Exception as e:
        print(f"Error sending SMS: {e}")
