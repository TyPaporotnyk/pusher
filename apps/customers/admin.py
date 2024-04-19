from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.core.exceptions import ValidationError

from apps.customers.models.categories import Category
from apps.customers.models.customers import Customer
from apps.customers.models.groups import Group, GroupKeyword
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
        queryset=GroupKeyword.objects.all(),
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

    def clean(self):
        max_pack = self.cleaned_data["max_pack"]

        if len(self.cleaned_data["groups"]) > max_pack:
            raise ValidationError({"groups": "Количество выбранных элементов больше, чем значение в поле max_pack."})

        if len(self.cleaned_data["groups_keywords"]) > max_pack:
            raise ValidationError(
                {"groups_keywords": "Количество выбранных элементов больше, чем значение в поле max_pack."}
            )

        if len(self.cleaned_data["keywords"]) > max_pack:
            raise ValidationError({"keywords": "Количество выбранных элементов больше, чем значение в поле max_pack."})


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "username", "posts_received"]
    readonly_fields = ["pk", "telegram_id", "registration_date", "posts_received"]
    search_fields = ["name", "username"]
    form = CustomerAdminForm


admin.site.register(Category)
admin.site.register(Group)
admin.site.register(GroupKeyword)
admin.site.register(Keyword)
admin.site.register(RealEstate)
