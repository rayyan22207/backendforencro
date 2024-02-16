from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile, StatusModel
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('blocked', 'restricted', 'used_to_be_friends', 'Friends', 'user')

class StatusModelForm(forms.ModelForm):
    class Meta:
        model = StatusModel
        fields = ['status']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        
        # Perform validation for the 'status' field here, if needed.
        # For example, you can check if the status is not empty.
        if not status:
            raise forms.ValidationError("Status cannot be empty.")
