from django import forms

from users.models import Device


class RegisterDeviceForm(forms.ModelForm):
    """Form to register a new device for the user.
    Check out `users.views.DeviceRegisterView` for an explanation on how
    the token exchange works."""
    token = forms.CharField(max_length=128, min_length=128)

    class Meta:
        model = Device
        fields = ['token', 'name', 'application', 'release']
