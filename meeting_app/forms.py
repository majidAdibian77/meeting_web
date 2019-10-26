from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from meeting_app.models import Event, ContactUs, UserProfileInfo


class UserForm(UserCreationForm):
    username = forms.CharField(label="نام کاربری", widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=True)
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)
    password2 = forms.CharField(label='تایید رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)
    first_name = forms.CharField(label='نام (اختیاری)', max_length=15, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='نام خانوادگی (اختیاری)', max_length=15, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='ایمیل', max_length=254, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')


class UserInfoForm(UserCreationForm):
    password1 = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)
    password2 = forms.CharField(label='تایید رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)
    first_name = forms.CharField(label='نام (اختیاری)', max_length=15, required=False,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='نام خانوادگی (اختیاری)', max_length=15, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='ایمیل', max_length=254, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('password1', 'password2', 'first_name', 'last_name', 'email')

    # def __init__(self, *args, **kwargs):
    #     super(UserCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['class'] = 'form-control'
    #     self.fields['username'].widget.attrs['label'] = 'نام کاربری'


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('profile_pic',)
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs['class'] = 'form-control'
        self.fields['profile_pic'].label = 'عکس خود را آپلود کنید (اختیاری)'


# class UserForm(UserCreationForm):
#     username = forms.CharField(label="نام کاربری", widget=forms.TextInput(attrs={'class': 'form-control'}),
#                                required=True)
#     password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#                                 required=True)
#     password2 = forms.CharField(label="تایید رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#                                 required=True)
#     email = forms.EmailField(label="ایمیل", max_length=254, required=True,
#                              widget=forms.TextInput(attrs={'class': 'form-control'}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'password1', 'password2', 'email')


class EventForm(forms.ModelForm):
    title = forms.CharField(label="عنوان", widget=forms.TextInput(attrs={'class': 'form-control'}),
                            required=True)
    note = forms.CharField(label="یادداشت", widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)

    class Meta:
        model = Event
        fields = ('title', 'note')


class EventCasesForm(forms.ModelForm):
    name = forms.CharField(label="نام مورد", widget=forms.TextInput(attrs={'class': 'form-control'}),
                           required=True)
    start_time = forms.TimeField(label='زمان شروع', widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 required=False)
    end_time = forms.TimeField(label='زمان پایان', widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=False)
    location = forms.CharField(label='مکان', widget=forms.TextInput(attrs={'class': 'form-control'}),
                               required=False)

    class Meta:
        model = Event
        fields = ('title', 'note', 'start_time', 'end_time', 'location')


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


# class UserInfoForm(forms.ModelForm):
#     # username = forms.CharField(label="نام کاربری", widget=forms.TextInput(attrs={'class': 'form-control'}),
#     #                            required=True)
#     first_name = forms.EmailField(label="نام", max_length=254, required=False,
#                                   widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(label="نام خانوادگی", widget=forms.TextInput(attrs={'class': 'form-control'}),
#                                 required=False)
#     password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#                                 required=True)
#     password2 = forms.CharField(label="تایید رمز عبور", widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#                                 required=True)
#     email = forms.EmailField(label="ایمیل", max_length=254, required=True,
#                              widget=forms.TextInput(attrs={'class': 'form-control'}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')

    # def __init__(self, *args, **kwargs):
    #     super(UserCreationForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['class'] = 'form-control'
    #     self.fields['username'].label = 'نام کاربری'
