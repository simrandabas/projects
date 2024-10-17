from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DonorRegistrationForm

def register_donor(request):
    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the donor to the database
            messages.success(request, 'Donor registered successfully!')
            return redirect('donor_success')  # Redirect to a success page
    else:
        form = DonorRegistrationForm()

    return render(request, 'donor/register.html', {'form': form})
