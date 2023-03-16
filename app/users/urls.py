from django.urls import path

from users import views

app_name = "users"
urlpatterns = [
    path("updatenames/", views.UpdateUserNameView.as_view(), name="updatenames"),
    path("updateemail/", views.UpdateUserEmailView.as_view(), name="updateemail"),
    path(
        "updatepassword/",
        views.UpdateUserPasswordView.as_view(),
        name="updatepassword"
    ),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("device/register/<str:payload>/", views.DeviceRegisterView.as_view(),
         name="device-register"),
]
