import base64
import json

from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, UpdateView
from users.forms import (
    RegisterDeviceForm,
    UserNameUpdateForm,
    UserEmailUpdateForm,
    UserPasswordUpdateForm,
)
from sorbay.keycloak import KeycloakAPI


class UpdateUserNameView(LoginRequiredMixin, UpdateView):
    template_name = "users/update-name.html"
    form_class = UserNameUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        first_name = user.first_name
        last_name = user.last_name
        payload = {'firstName': first_name, 'lastName': last_name}
        keycloakAPI = KeycloakAPI()
        keycloak_admin = keycloakAPI.keycloak_admin
        keycloak_admin.refresh_token()
        response = keycloak_admin.update_user(user_id=user.username, payload=payload)
        if response:
            raise ValidationError("An error occured, please try again later...")
        form.save(commit=True)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("users:settings")


class UpdateUserEmailView(LoginRequiredMixin, UpdateView):
    template_name = "users/update-email.html"
    form_class = UserEmailUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        email = user.email
        payload = {'username': email, 'email': email}
        keycloakAPI = KeycloakAPI()
        keycloak_admin = keycloakAPI.keycloak_admin
        keycloak_admin.refresh_token()
        response = keycloak_admin.update_user(user_id=user.username, payload=payload)
        if response:
            raise ValidationError("An error occured, please try again later...")
        form.save(commit=True)
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("users:settings")


class UpdateUserPasswordView(LoginRequiredMixin, UpdateView):
    template_name = "users/update-password.html"
    form_class = UserPasswordUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.data['new_password1']
        keycloakAPI = KeycloakAPI()
        keycloak_admin = keycloakAPI.keycloak_admin
        keycloak_admin.refresh_token()
        response = keycloak_admin.set_user_password(
            user_id=user.username,
            password=password,
            temporary=False
        )
        if response:
            raise ValidationError("An error occured, please try again later...")
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("users:settings")


class SettingsView(LoginRequiredMixin, TemplateView):
    """View to display a users setting page"""
    template_name = "users/settings.html"


class DeviceRegisterView(LoginRequiredMixin, FormView):
    """View for a user to register/link a new device to his account. Currently, that's
    going to be the desktop app.

    A typical flow might look like this:
     - desktop app creates a token locally and adds some payload (computer name, app name,
       release)
     - desktop app encodes the payload as base64 and opens a browser window pointing
       to this view
     - this view decodes the payload and creates a form containing the payload as initial
       data
     - the view gets rendered via GET, containing the form data from the payload. The
       actual form data is invisible. The user only sees the forms corresponding submit
       button, telling him to link his desktop app to his account.
     - on form submit via POST, we validate the form data and create a new device. By
       default, the new device has `has_key_exchanged` set to false.
     - this view then displays a message that his app has been linked to his account.
     - in the background, the app constantly queries the API using the token it provided
       earlier in the payload. Once the device is registered, the API returns an API key
       for the desktop app and sets `has_key_exchanged` to true so that the key can no
       longer be exchanged based on the device id alone.
     - the desktop app saves the API key and logs the user in
    """
    template_name = "users/register-device.html"
    form_class = RegisterDeviceForm

    def get_initial(self):
        """This function fills the intial form data based on the payload it received
        in the URL"""
        try:
            data = json.loads(base64.b64decode(self.kwargs['payload']))
            return {
                "token": data.get("token"),
                "name": data.get("name"),
                "application": data.get("application"),
                "release": data.get('release')
            }
        # todo: catching a too broad exception here, refactor
        except Exception:
            pass
        return {}

    def form_valid(self, form):
        device = form.save(commit=False)
        device.user = self.request.user
        device.save()
        return render(
            context={"form_processed": True, "success": True, "form": form},
            template_name=self.get_template_names(),
            request=self.request
        )

    def form_invalid(self, form):
        return render(
            context={"form_processed": True, "success": False, "form": form},
            template_name=self.get_template_names(),
            request=self.request
        )
