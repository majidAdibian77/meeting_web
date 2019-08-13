from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from meeting_app.models import Event, ContactUs


class UserForm(UserCreationForm):
    username = forms.CharField(label="نام کاربری", widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)
    password2 = forms.CharField(label="تایید رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)
    email = forms.EmailField(label="ایمیل", max_length=254, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class EventForm(forms.ModelForm):
    title = forms.CharField(label="عنوان", widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    note = forms.CharField(label="یادداشت", widget=forms.TextInput(attrs={'class': 'form-control'}),
                                required=True)
    location = forms.CharField(label="مکان", widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'location'}),
                                required=True)

    class Meta:
        model = Event
        fields = ('title', 'note', 'location')


class ContactUsForm(forms.ModelForm):
    name = forms.CharField(label="نام", widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    email = forms.EmailField(label="ایمیل", max_length=254, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label="متن پیام", widget=forms.TextInput(attrs={'class': 'form-control'}),
                                required=True)

    class Meta:
        model = ContactUs
        fields = ('name', 'text', 'email')