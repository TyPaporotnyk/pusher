from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserChangeForm

from apps.common.models import Blacklist, Group, Keyword
from apps.customers.models import Customer


class CustomerChangeForm(UserChangeForm):

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=widgets.FilteredSelectMultiple("Groups", is_stacked=False),
        required=False,
    )
    groups_keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        widget=widgets.FilteredSelectMultiple("GroupKeywords", is_stacked=False),
        required=False,
    )
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.all(),
        widget=widgets.FilteredSelectMultiple("Keywords", is_stacked=False),
        required=False,
    )
    blacklist = forms.ModelMultipleChoiceField(
        queryset=Blacklist.objects.all(),
        widget=widgets.FilteredSelectMultiple("Blacklist", is_stacked=False),
        required=False,
    )

    class Meta:
        model = Customer
        fields = "__all__"
