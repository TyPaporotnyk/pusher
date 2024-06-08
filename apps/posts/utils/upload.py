def get_post_image_path(instance, file) -> str:
    return f"posts/{instance.post.id}/images/{file}"
