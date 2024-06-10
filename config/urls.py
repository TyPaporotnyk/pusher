from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Pusher Admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.routes", namespace="api_v1")),
    path("import/", include("apps.import.urls", namespace="import")),
]
