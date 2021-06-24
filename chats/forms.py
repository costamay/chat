from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import *

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add valid email Address')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        
    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Invalid login')
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['profile_picture', 'first_name', 'last_name', 'bio']
                  
    def clean_profile_picture(self):
        if self.is_valid():
            profile_picture = self.cleaned_data['profile_picture']
            try:
                profile = Profile.objects.exclude(pk=self.instance.pk).get(profile_picture=profile_picture)
            except Profile.DoesNotExist:
                return profile_picture
            raise forms.ValidationError('Profile image "%s" is already in use.' % profile_picture)