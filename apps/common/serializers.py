from rest_framework import serializers

from apps.common.models import Blacklist, Category, Group, Keyword


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class GroupSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Group
        fields = ["id", "url", "category", "is_active"]


class KeywordSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Keyword
        fields = ["id", "name", "category", "is_active"]


class BlacklistSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Blacklist
        fields = ["id", "name", "category", "is_active"]
