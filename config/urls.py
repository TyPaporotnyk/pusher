from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Pusher Admin"

urlpatterns = [
    path("jet/", include("jet.urls", "jet")),
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.routes")),
]
