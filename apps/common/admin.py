from django.contrib import admin

from apps.common.models import Blacklist, Category, Group, Keyword

admin.site.register(Category)
admin.site.register(Blacklist)
admin.site.register(Group)
admin.site.register(Keyword)
