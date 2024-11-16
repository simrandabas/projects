
# include the ml matching algo
# notification/matching.py
from .utils import send_notification_sms

def calculate_urgency_score(waiting_time, severity, age, tissue_match):
    """
    Calculate the urgency score for the recipient.
    
    Parameters:
    - waiting_time (int): Time in days the recipient has been on the waiting list.
    - severity (int): The severity of the recipient's condition (1-10).
    - age (int): The age of the recipient (years).
    - tissue_match (int): A score (1-100) representing how well the tissue matches between donor and recipient.
    
    Returns:
    - float: The urgency score calculated based on the parameters.
    """
    # Defining weights based on the importance of each factor
    # You can adjust these weights based on your medical priorities
    urgency_score = (waiting_time * 0.3) + (severity * 0.4) + ((100 - age) * 0.2) + (tissue_match * 0.1)
    
    return urgency_score
# notification/matching.py

def is_compatible(donor_blood, recipient_blood):
    """
    Check if a donor's blood type is compatible with a recipient's blood type.
    
    Parameters:
    - donor_blood (str): The blood type of the donor (e.g., "O+", "A-", "B+").
    - recipient_blood (str): The blood type of the recipient (e.g., "O+", "A-", "B+").
    
    Returns:
    - bool: True if the donor and recipient blood types are compatible, False otherwise.
    """
    # Blood type compatibility rules
    compatibility = {
        "O+": ["O+", "A+", "B+", "AB+"],
        "O-": ["O+", "A+", "B+", "AB+", "O-"],
        "A+": ["A+", "AB+"],
        "A-": ["A+", "AB+", "A-", "O-"],
        "B+": ["B+", "AB+"],
        "B-": ["B+", "AB+", "B-", "O-"],
        "AB+": ["AB+"],
        "AB-": ["AB+", "AB-"]
    }
    
    return recipient_blood in compatibility.get(donor_blood, [])
# notification/matching.py

def match_donor_to_recipient(donors, recipients):
    """
    Match donors to recipients based on urgency score and blood type compatibility.
    
    Parameters:
    - donors (list of dict): A list of donor objects, each containing id, blood_type, organ, etc.
    - recipients (list of dict): A list of recipient objects, each containing id, organ_required, waiting_time, etc.
    
    Returns:
    - list of dict: A list of matched donor-recipient pairs with urgency scores.
    """
    matched_pairs = []

    # Step 1: Sort recipients by urgency score (highest first)
    sorted_recipients = sorted(recipients, key=lambda x: x['urgency_score'], reverse=True)

    for recipient in sorted_recipients:
        for donor in donors:
            # Step 2: Check if the donor's organ type matches the recipient's required organ
            # and if their blood types are compatible
            if recipient['organ_required'] == donor['organ'] and is_compatible(donor['blood_type'], recipient['blood_type']):
                # If a match is found, add it to matched_pairs
                matched_pair = {
                    "donor_id": donor['id'],
                    "recipient_id": recipient['id'],
                    "organ": donor['organ'],
                    "urgency_score": recipient['urgency_score']
                }
                matched_pairs.append(matched_pair)
                
                # Send notification emails to both donor and recipient
                send_notification_sms(donor, recipient)
                
                donors.remove(donor)  # Remove the matched donor from the list
                break  # Move to the next recipient

    return matched_pairs
# notification/matching.py

def match_urgency_based(donors, recipients):
    """
    First calculates the urgency score for each recipient, then matches them with compatible donors
    based on organ compatibility, blood type compatibility, and urgency.
    
    Parameters:
    - donors (list of dict): A list of donor objects.
    - recipients (list of dict): A list of recipient objects.
    
    Returns:
    - list of dict: A list of matched donor-recipient pairs.
    """
    # Step 1: Calculate urgency score for each recipient
    for recipient in recipients:
        recipient['urgency_score'] = calculate_urgency_score(
            recipient['waiting_time'], recipient['severity'], recipient['age'], recipient['tissue_match']
        )
    
    # Step 2: Match donors and recipients
    return match_donor_to_recipient(donors, recipients)