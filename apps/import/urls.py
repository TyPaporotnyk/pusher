from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "import"

urlpatterns = [
    path(
        "success/",
        TemplateView.as_view(template_name="import/success_import_template.html"),
        name="success",
    ),
    path("keywords/", views.import_keywords_view, name="keywords"),
    path("groups/", views.import_groups_view, name="groups"),
    path("blacklists/", views.import_black_list_view, name="black-lists"),
    path("public-keywords/", views.import_public_keywords_view, name="public-keywords"),
    path("public-groups/", views.import_public_groups_view, name="public-groups"),
    path("public-blacklists/", views.import_public_black_list_view, name="public-black-lists"),
]
