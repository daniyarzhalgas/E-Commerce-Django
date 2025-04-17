from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("products.urls")),
    path("api/", include("products.api_urls")),
]



if settings.DEBUG:  # Serve media files only in development mode
    urlpatterns