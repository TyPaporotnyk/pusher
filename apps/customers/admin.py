from django import forms
from django.contrib import admin
from django.contrib.admin import widgets

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
        label="Groups",
        widget=widgets.FilteredSelectMultiple("GroupKeywordS", is_stacked=False),
        required=False,
    )
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        label="Keywords",
        widget=widgets.FilteredSelectMultiple("Keywords", is_stacked=False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CustomerAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields["groups"].initial = self.instance.groups.all()
            self.fields["keywords"].initial = self.instance.keywords.all()
            self.fields["groups_keywords"].initial = self.instance.groups_keywords.all()


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
