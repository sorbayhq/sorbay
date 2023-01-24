from django.urls import reverse
from django.views.generic import RedirectView
from django.conf import settings


class HomeView(RedirectView):
    """Simple view to redirect a user to the dashboard or login screen
    (if not authenticated)"""

    def get_redirect_url(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return settings.LOGIN_REDIRECT_URL
        return reverse("recordings:dashboard")
