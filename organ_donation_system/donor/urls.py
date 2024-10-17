from django.contrib import admin
from django.urls import path
from donor import views

urlpatterns = [
    path("", views.register_donor, name='donor')
]
