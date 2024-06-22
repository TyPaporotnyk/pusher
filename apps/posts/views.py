from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.posts.serializers import PostSerializer
from apps.posts.services import PostService


@extend_schema(tags=["Posts"])
class PostView(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        return PostService().get_all()
