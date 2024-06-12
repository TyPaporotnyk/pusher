from django.contrib import admin

from apps.posts.models import Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id",)
    inlines = [PostImageInline]
