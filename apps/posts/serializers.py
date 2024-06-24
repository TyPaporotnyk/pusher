from rest_framework import serializers

from apps.posts.models import Post, PostImage
from apps.posts.services import PostService
from apps.posts.task import link_post_to_users_task, load_post_images_task


class PostSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=serializers.URLField(), required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "url",
            "description",
            "actor_name",
            "actor_url",
            "group_name",
            "group_url",
            "images",
            "created_at",
        )

    def validate_description(self, value):
        if PostService().get_by(description=value).exists():
            raise serializers.ValidationError("Post with this description already exists.")

        return value

    def create(self, validated_data):
        images_data = validated_data.pop("images", [])
        post = Post.objects.create(**validated_data)
        post.save()

        for image_url in images_data:
            post_image = PostImage(post=post, original_image_url=image_url)
            post_image.save()

        link_post_to_users_task.apply_async(kwargs={"post_id": post.id}, countdown=1)
        load_post_images_task.apply_async(kwargs={"post_id": post.id}, countdown=1)

        return post
