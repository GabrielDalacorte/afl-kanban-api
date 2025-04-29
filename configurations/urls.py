from django.contrib import admin
from django.urls import include, path
from apps.users.token import CustomObtainAuthToken
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
]

API_PREFIX = "api/v1/"

urlpatterns += [
    path(f"{API_PREFIX}", include("apps.routes.api_router"), name="api"),
    path(f"{API_PREFIX}rest-auth/login/", CustomObtainAuthToken.as_view(), name="auth-token"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    