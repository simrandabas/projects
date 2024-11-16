# notifications/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('match/', views.match_donors_and_recipients, name='match_donors_and_recipients'),
]
