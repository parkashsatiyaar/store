from django import forms
from django.forms import fields, widgets

from .models import Account, UserProfile


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "First Name"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': "Last Name"}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': "Email"}))
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': "Phone No"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'pattern': "(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}",
        'title': "Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'email', 'phone_number', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={
                                       'invalid': {"Image files only"}}, widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city',
                  'state', 'country', 'profile_picture')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
