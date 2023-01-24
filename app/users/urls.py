from django.urls import path

from users import views

app_name = "users"
urlpatterns = [
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("device/register/<str:payload>/", views.DeviceRegisterView.as_view(),
         name="device-register"),
]
