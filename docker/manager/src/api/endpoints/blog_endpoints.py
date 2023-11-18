import logging

from django.conf import settings
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.connectors import FeedConnector
from api.mixins import BlogsMixin
from api.serializers.blog_serializers import BlogModelSerializer
from api.serializers.common import ModelUidSerializer
from manager.models import Blog, BlogTag


logger = logging.getLogger(__name__)


class BlogViewset(viewsets.ModelViewSet):
    serializer_class = BlogModelSerializer
    queryset = Blog.objects.all()
    lookup_field = 'uid'
    authentication_classes = settings.AUTHENTICATION_CLASSES
    permission_classes = settings.PERMISSION_CLASSES


    def destroy(self, request, uid=None):
        try:
            blog = Blog.objects.get(uid=uid)
        except Blog.DoesNotExist:
            return Response(
                data=dict(error="Blog does not exist"), 
                status=400
            )
        blog_url = blog.url
        blog_name = blog.name
        blog.delete()
        FeedConnector.update_blogs()
        return Response(
            data=dict(
                message="%s | %s deleted" % (
                    blog_name, 
                    blog_url
                )
            ),
            status=200
        )



