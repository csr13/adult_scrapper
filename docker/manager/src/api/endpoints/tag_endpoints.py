from django.conf import settings

from rest_framework import viewsets

from api.serializers.tag_serializers import BlogTagModelSerializer
from manager.models import BlogTag


class BlogTagsViewset(viewsets.ModelViewSet):
    serializer_class = BlogTagModelSerializer
    queryset = BlogTag.objects.all()
    lookup_field = 'uid'
    authentication_classes = settings.AUTHENTICATION_CLASSES
    permission_classes = settings.PERMISSION_CLASSES
