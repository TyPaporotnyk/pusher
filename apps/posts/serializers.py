from rest_framework import serializers

from apps.posts.models import Post, PostImage
from apps.posts.task import link_post_to_users_task, load_post_images_task


class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField("get_image_urls")

    class Meta:
        model = Post
        fields = (
            "id",
            "url",
            "description",
            "group_name",
            "group_url",
            "images",
            "created_at",
            "updated_at",
        )

    @staticmethod
    def get_image_urls(obj):
        return [image.image.url for image in obj.images.all()]


class PostCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=serializers.URLField(), required=False)

    class Meta:
        model = Post
        fields = ("description", "url", "group_name", "group_url", "images")

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        post = Post.objects.create(**validated_data)

        for image_url in images_data:

            post_image = PostImage(post=post, original_image_url=image_url)
            post_image.save()

        link_post_to_users_task.delay(post_id=post.id)
        load_post_images_task.delay(post_id=post.id)

        return post
