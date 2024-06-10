from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.customers.forms import CustomerChangeForm
from apps.customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    change_form_template = "admin/customers/change_form_template.html"
    form = CustomerChangeForm

    list_display = ("username", "first_name", "last_name")
    list_display_links = ("username", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_admin", "is_superuser")}),
        ("Parser settings", {"fields": ("max_pack", "groups", "groups_keywords", "keywords", "blacklist")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    filter_horizontal = ()
    ordering = ()
    list_filter = ()
