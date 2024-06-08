from rest_framework import serializers

from apps.posts.models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = PostImage
        fields = ("id", "url")

    def get_image_url(self, obj):
        return obj.image.url


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True)

    class Meta:
        model = Post
        fields = ("id", "url", "title", "description", "slug", "images")
