from django import forms
from django.core.exceptions import ValidationError

from users.models import Device, User


class RegisterDeviceForm(forms.ModelForm):
    """Form to register a new device for the user.
    Check out `users.views.DeviceRegisterView` for an explanation on how
    the token exchange works."""
    token = forms.CharField(max_length=128, min_length=128)

    class Meta:
        model = Device
        fields = ['token', 'name', 'application', 'release']


class UserNameUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserEmailUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']


class UserPasswordUpdateForm(forms.ModelForm):

    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2 and (password1 != password2):
            raise ValidationError('Password Missmach')
        return password2
