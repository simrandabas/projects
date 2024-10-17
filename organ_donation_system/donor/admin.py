from django.contrib import admin
from donor.models import donors

admin.site.register(donors)
class DonorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'contact_number', 'date_of_birth', 'gender', 'blood_group', 'organ_to_donate', 'address']
