from django.contrib import admin

from apps.bot.models.photos import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("photo_url", "created_at")
    readonly_fields = (
        "photo_id",
        "created_at",
    )
