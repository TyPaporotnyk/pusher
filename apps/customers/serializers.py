from rest_framework import serializers

from apps.common.serializers import KeywordSerializer
from apps.customers.models import Customer, CustomerPost
from apps.customers.services.customers import CustomerService
from apps.posts.serializers import PostSerializer


class ActiveGroupsKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return CustomerService(customer=self.context["request"].user).group_service.get_all_active()


class ActiveKeywordKeyRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return CustomerService(customer=self.context["request"].user).keyword_service.get_all_active()


class ActiveBlackListRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        return CustomerService(customer=self.context["request"].user).black_list_service.get_all_active()


class CustomerSerializer(serializers.ModelSerializer):
    groups = ActiveGroupsKeyRelatedField(many=True)
    keywords = ActiveKeywordKeyRelatedField(many=True)
    black_lists = ActiveBlackListRelatedField(many=True)

    class Meta:
        model = Customer
        fields = ("id", "first_name", "last_name", "username", "email", "groups", "keywords", "black_lists")

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        customer_service = CustomerService(customer=instance)

        ret["groups"] = customer_service.group_service.get_all_active()
        ret["keywords"] = customer_service.keyword_service.get_all_active()
        ret["black_lists"] = customer_service.black_list_service.get_all_active()
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
