from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path, re_path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from django.views.decorators.csrf import ensure_csrf_cookie


@ensure_csrf_cookie
def index_view(request):
    from django.shortcuts import render
    return render(request, 'index.html')


def obtain_csrf_token(request):
    from django.http import JsonResponse
    from django.middleware.csrf import get_token
    return JsonResponse({'csrfToken': get_token(request)})


urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# API URLS
urlpatterns += [
    # User management
    path("api/users/", include("backend.users.urls", namespace="users")),
    path("api/listings/", include("backend.listings.urls", namespace="listings")),
    path("api/accounts/", include("allauth.urls")),
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token, name="obtain_auth_token"),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path("_allauth/", include("allauth.headless.urls")),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

urlpatterns += [
    # csrf token expose for frontend dev
    path("api/csrf/", obtain_csrf_token, name="api-csrf"),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        *urlpatterns,
    ]

urlpatterns += [
    # render index.html for all other paths
    re_path(r'^.*', index_view, name='index'),
]
