from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import User, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True,
            widget=forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control',
            }))
    username = forms.CharField(
            widget=forms.TextInput(attrs={
                'placeholder': 'Username',
                'class': 'form-control',
            }))
    password1 = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'placeholder': 'Password',
                'class': 'form-control',
            }))
    password2 = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'placeholder': 'Confirm Password',
                'class': 'form-control',
            }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
        }))
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'website']
        
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a short bio'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Website'
            })
            }