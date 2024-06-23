from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserChangeForm

from apps.common.models import Blacklist, Group, Keyword
from apps.customers.models import Customer


class CustomerChangeForm(UserChangeForm):

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.none(),
        widget=widgets.FilteredSelectMultiple("Groups", is_stacked=False),
        required=False,
    )
    keywords = forms.ModelMultipleChoiceField(
        queryset=Keyword.objects.none(),
        widget=widgets.FilteredSelectMultiple("Keywords", is_stacked=False),
        required=False,
    )
    black_lists = forms.ModelMultipleChoiceField(
        queryset=Blacklist.objects.none(),
        widget=widgets.FilteredSelectMultiple("Blacklist", is_stacked=False),
        required=False,
    )

    class Meta:
        model = Customer
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CustomerChangeForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["groups"].queryset = self.instance.groups.all()
            self.fields["groups"].initial = self.instance.groups.all().filter(is_active=True)

            self.fields["keywords"].queryset = self.instance.keywords.all()
            self.fields["keywords"].initial = self.instance.keywords.all().filter(is_active=True)

            self.fields["black_lists"].queryset = self.instance.black_lists.all()
            self.fields["black_lists"].initial = self.instance.black_lists.all().filter(is_active=True)

    def save(self, commit=True):
        instance = super(CustomerChangeForm, self).save(commit=commit)

        instance.groups.update(is_active=False)
        for group in self.cleaned_data["groups"]:
            group.is_active = True
            group.save()

        instance.keywords.update(is_active=False)
        for keyword in self.cleaned_data["keywords"]:
            keyword.is_active = True
            keyword.save()

        instance.black_lists.update(is_active=False)
        for black_list in self.cleaned_data["black_lists"]:
            black_list.is_active = True
            black_list.save()

        return instance
