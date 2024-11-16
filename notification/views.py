from django.shortcuts import render
from django.http import JsonResponse
from donor.models import donors 
from recipient.models import recipients
from .models import  recipients  # Import models
from .utils import send_notification_sms  # Import your notification function
from .matching import match_urgency_based
from datetime import date

def calculate_age(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def match_donors_and_recipients(request):
    # Fetch donors and recipients from the database
    donors_data = [
        {
            "id": d.id,
            "blood_type": d.blood_group,
            "organ": d.organ_to_donate,
            "location": d.address,
            "age": calculate_age(d.date_of_birth),
            "name": d.full_name,
            "phone": d.contact_number,  # Add phone field
        } 
        for d in donors.objects.all()
    ]

    recipients_data = [
        {
            "id": r.id,
            "blood_type": r.blood_group,
            "organ_required": r.organ_needed,
            "location": r.address,
            "waiting_time": r.waiting_time,  
            "severity": getattr(r, 'severity', 0),
            "age": calculate_age(r.date_of_birth),
            "tissue_match": getattr(r, 'tissue_match', 0),
            "name": r.full_name,
            "phone": r.contact_number,  # Add phone field
        } 
        for r in recipients.objects.all()
    ]

    # Find matches
    matched_pairs = match_urgency_based(donors_data, recipients_data)
    
    # Send SMS notifications for each match
    for match in matched_pairs:
        if match and "donor_id" in match and "recipient_id" in match:
            donor = next((d for d in donors_data if d["id"] == match["donor_id"]), None)
            recipient = next((r for r in recipients_data if r["id"] == match["recipient_id"]), None)
            
            if donor and recipient:
                send_notification_sms(donor, recipient)
    
    return JsonResponse(matched_pairs, safe=False)
