from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.customers.forms import CustomerChangeForm
from apps.customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    change_form_template = "admin/customers/change_form_template.html"
    form = CustomerChangeForm

    list_display = ("username", "first_name", "last_name", "match_post_count", "is_active")
    list_display_links = ("username", "first_name", "last_name")
    readonly_fields = (
        "last_login",
        "date_joined",
        "telegram_id",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("email", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_active", "is_admin", "is_staff", "is_superuser")}),
        ("Parser settings", {"fields": ("max_pack", "groups", "keywords", "blacklist")}),
        ("Important datas", {"fields": ("telegram_id", "last_login", "date_joined")}),
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
