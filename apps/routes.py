from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("customers/", include("apps.customers.urls")),
    path("posts/", include("apps.posts.urls")),
    path("common/", include("apps.common.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
