from rest_framework import serializers

from apps.common.models import Blacklist, Category, Group, Keyword


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name"]


class GroupSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ["id", "url", "category"]


class KeywordSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Keyword
        fields = ["id", "name", "category"]


class BlacklistSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Blacklist
        fields = ["id", "name", "category"]
