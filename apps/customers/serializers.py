from rest_framework import serializers

from apps.common.serializers import KeywordSerializer
from apps.customers.models import Customer, CustomerPost
from apps.customers.services import CustomerService
from apps.posts.serializers import PostSerializer


class ActiveGroupsKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return CustomerService(request=self.context["request"]).get_customer_groups()


class ActiveKeywordKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return CustomerService(request=self.context["request"]).get_customer_keywords()


class ActiveBlackListKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return CustomerService(request=self.context["request"]).get_customer_black_list()


class CustomerSerializer(serializers.ModelSerializer):
    groups = ActiveGroupsKeyRelatedField(many=True)
    keywords = ActiveKeywordKeyRelatedField(many=True)
    black_lists = ActiveBlackListKeyRelatedField(many=True)

    class Meta:
        model = Customer
        fields = ("id", "first_name", "last_name", "username", "email", "groups", "keywords", "black_lists")

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        ret["groups"] = [group.id for group in instance.groups.filter(is_active=True)]
        ret["keywords"] = [keyword.id for keyword in instance.keywords.filter(is_active=True)]
        ret["black_lists"] = [black_lists.id for black_lists in instance.black_lists.filter(is_active=True)]
        return ret


class CustomerPostSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    keywords = KeywordSerializer(read_only=True, many=True)

    class Meta:
        model = CustomerPost
        fields = (
            "id",
            "post",
            "keywords",
            "created_at",
            "updated_at",
        )


class CustomerTelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("telegram_id",)
