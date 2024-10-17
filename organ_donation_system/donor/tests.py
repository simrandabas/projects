
from django.test import TestCase
from .models import donors
from datetime import date

class DonorModelTest(TestCase):
    def setUp(self):
        # Create a sample donor object
        self.donor = donors.objects.create(
            full_name="John Doe",
            email="john.doe@example.com",
            contact_number="1234567890",
            date_of_birth=date(1990, 1, 1),
            gender="M",
            blood_group="O+",
            organ_to_donate="Kidney",
            address="123 Main St, Springfield"
        )

    def test_donor_creation(self):
        # Test if the donor was created successfully
        donor = donors.objects.get(email="john.doe@example.com")
        self.assertEqual(donor.full_name, "John Doe")
        self.assertEqual(donor.gender, "M")
        self.assertEqual(donor.blood_group, "O+")
        self.assertEqual(donor.contact_number, "1234567890")
        self.assertEqual(donor.organ_to_donate, "Kidney")

    def test_donor_str(self):
        # Test the string representation of the donor
        donor = donors.objects.get(email="john.doe@example.com")
        self.assertEqual(str(donor), "John Doe")
