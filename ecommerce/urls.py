from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("products.urls")),
]



if settings.DEBUG:  # Serve media files only in development mode
    urlpatterns 