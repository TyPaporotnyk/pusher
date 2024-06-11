from rest_framework import serializers

from apps.base.exceptions.files import DownloadFileException
from apps.base.services.files import download_file
from apps.posts.models import Post, PostImage


class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField("get_image_urls")

    class Meta:
        model = Post
        fields = ("id", "url", "title", "description", "group_name", "group_url", "slug", "images")

    def get_image_urls(self, obj):
        return [image.image.url for image in obj.images.all()]


class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=serializers.URLField(), required=False)

    class Meta:
        model = Post
        fields = ("title", "description", "url", "group_name", "group_url", "images")

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        post = Post.objects.create(**validated_data)

        for image_url in images_data:
            try:
                post_image = PostImage(post=post)
                post_image.image.save(*download_file(image_url))
            except DownloadFileException:
                continue

        return post
