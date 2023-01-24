from django.conf import settings
from django.urls import include, path

from sorbay.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("recordings/", include("recordings.urls", namespace="recordings")),
    path("users/", include("users.urls", namespace="users")),
    path("api/v1/", include("sorbay.api.v1.urls", namespace="api")),
    path('oidc/', include('mozilla_django_oidc.urls')),
]

# if we are on the development environment, we want the django devserver to also
# serve the static files. Additionally, we want to have the django debug toolbar
# enabled
if settings.DEBUG:  # pragma: no cover
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    try:
        import debug_toolbar
        urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
    except ImportError:
        pass
