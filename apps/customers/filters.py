import django_filters

from apps.customers.models import CustomerPost


class CustomerPostFilter(django_filters.FilterSet):

    class Meta:
        model = CustomerPost
        fields = ["keywords__name"]
