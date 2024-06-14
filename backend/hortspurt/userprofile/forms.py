from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    # def 
    # save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.username = self.cleaned_data['email']
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']

    #     if commit:
    #         user.save()
        
    #     return user

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('gender',)