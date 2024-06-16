from django.contrib import admin

from apps.common.models import Blacklist, Category, Group, Keyword


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "customer")
    search_fields = ("name",)


@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "customer")
    list_filter = ("category",)
    search_fields = (
        "name",
        "category__name",
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("url", "category")
    list_filter = ("category",)
    search_fields = ("url", "category__name")


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "customer")
    list_filter = ("category",)
    search_fields = ("name", "category__name")
