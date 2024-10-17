from django import forms
from .models import donors

class DonorRegistrationForm(forms.ModelForm):
    class Meta:
        model = donors
        fields = ['full_name', 'email', 'contact_number', 'date_of_birth', 'gender', 'blood_group', 'organ_to_donate', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
