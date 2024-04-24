from django import forms
from django.contrib import admin
from django.contrib.admin import widgets

from apps.customers.models.categories import Category
from apps.customers.models.customers import Customer
from apps.customers.models.groups import Group
from apps.customers.models.keywords import Keyword
from apps.customers.models.real_estate import RealEstate


class CustomerAdminForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "username",
            "password",
            "max_pack",
        ]

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        label="Groups",
        widget=widgets.FilteredSelectMultiple("Groups", is_stacked=False),
        required=False,
    )
    groups_keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        label="GroupKeywords",
        widget=widgets.FilteredSelectMultiple("GroupKeywords", is_stacked=False),
        required=False,
    )
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        label="Keywords",
        widget=widgets.FilteredSelectMultiple("Keywords", is_stacked=False),
        required=False,
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    change_form_template = "admin/customers/customer/change_form.html"
    list_display = ["name", "username", "posts_received"]
    readonly_fields = ["pk", "telegram_id", "registration_date", "posts_received"]
    search_fields = ["name", "username"]
    form = CustomerAdminForm


@admin.register(RealEstate)
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ["real_estate_id", "website"]
    ordering = ["-created_at"]


admin.site.register(Category)
admin.site.register(Group)
admin.site.register(Keyword)
