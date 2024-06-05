from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("import-success/", TemplateView.as_view(template_name="customers/success_load.html"), name="import_success"),
    path("import-keywords/", views.import_keywords_view, name="import_keywords"),
    path("import-groups/", views.import_groups_view, name="import_groups"),
]
