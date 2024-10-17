

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class SignupPageTestCase(TestCase):
    
    def test_user_signup(self):
        """Test if a user can sign up successfully with matching passwords."""
        
        signup_url = reverse('SignupPage')
        
        # User data for signup
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123',
        }
        
        # Send a POST request with the user data
        response = self.client.post(signup_url, user_data)
        
        # Check if the response redirects to the login page after successful signup
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))  # Assuming 'login' is the name of the login view
        
        # Check if the user was created in the database
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)

