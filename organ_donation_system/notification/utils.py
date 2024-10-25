from django.core.mail import send_mail
from django.conf import settings

def send_notification_email(donor, recipient):
    subject = 'Organ Match Found'
    message_donor = f"Hello {donor.name},\n\nA recipient has been found for your donation of {donor.organ}."
    message_recipient = f"Hello {recipient.name},\n\nA donor has been found for the organ you need: {recipient.organ}."
    email_from = settings.EMAIL_HOST_USER

    send_mail(subject, message_donor, email_from, [donor.email])
    send_mail(subject, message_recipient, email_from, [recipient.email])
