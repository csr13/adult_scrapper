import logging

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from api.serializers.common import ItemExistsResponseSerializer
from api.serializers.image_serializers import ImageSerializer
from manager.models import DirtyImage


logger = logging.getLogger(__name__)


class ImagesViewset(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    queryset = DirtyImage.objects.all()    
    lookup_field = 'uid'
    permission_classes = settings.PERMISSION_CLASSES
    authentication_classes = settings.AUTHENTICATION_CLASSES

    def destroy(self, request, uid=None):
        try:
            image = DirtyImage.objects.get(uid=uid)
        except DirtyImage.DoesNotExist:
            return Response(data=dict(error="Image does not exist"), status=400)
        image.delete()
        return Response(data=dict(message="Image deleted"), status=200)


    @action(
        detail=False, 
        url_path='image-exists/(?P<name>\w+)', 
        url_name='image_exists',
        methods=["get"],
        serializer_class=ItemExistsResponseSerializer
    )
    def image_exists(self, request, name):
        exists = DirtyImage.objects.filter(name=name).exists()
        return Response(
            data=dict(exists=exists), 
            status=200
        )
