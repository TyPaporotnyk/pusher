from django.contrib import admin

from apps.posts.models import Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    list_display_links = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PostImageInline]
