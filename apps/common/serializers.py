from rest_framework import serializers

from apps.common.models import Blacklist, Category, Group, Keyword
from apps.customers.services import CustomerService


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class GroupSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False)

    class Meta:
        model = Group
        fields = ["id", "url", "category", "is_active"]

    def create(self, validated_data):
        category_name = validated_data.get("category")

        if category_name is not None:
            category, _ = Category.objects.get_or_create(
                name=category_name.strip(),
                customer=CustomerService(self.context.get("request")).get_customer(),
            )
            validated_data["category"] = category

        return super().create(validated_data)


class KeywordSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False)

    class Meta:
        model = Keyword
        fields = ["id", "name", "category", "is_active"]

    def create(self, validated_data):
        category_name = validated_data.get("category")

        if category_name is not None:
            category, _ = Category.objects.get_or_create(
                name=category_name.strip(),
                customer=CustomerService(self.context.get("request")).get_customer(),
            )
            validated_data["category"] = category

        return super().create(validated_data)


class BlacklistSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False)

    class Meta:
        model = Blacklist
        fields = ["id", "name", "category", "is_active"]

    def create(self, validated_data):
        category_name = validated_data.get("category")

        if category_name is not None:
            category, _ = Category.objects.get_or_create(
                name=category_name.strip(),
                customer=CustomerService(self.context.get("request")).get_customer(),
            )
            validated_data["category"] = category

        return super().create(validated_data)
