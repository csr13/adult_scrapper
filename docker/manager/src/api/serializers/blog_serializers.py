from rest_framework import serializers

from api.connectors import FeedConnector
from api.mixins import BlogsMixin
from manager.models import Blog

   
class BlogModelSerializer(
    BlogsMixin, 
    serializers.ModelSerializer
):
    categories = serializers.StringRelatedField(
        many=True, 
        read_only=True
    ) 
    class Meta:
        model = Blog
        fields = [
            'pk', 
            'uid', 
            'created_at', 
            'name', 
            'url',
            'categories'
        ]
        read_only_fields = [
            'uid', 
            'images', 
            'tags', 
            'pk',
            'categories'
        ] 


    def create(self, validated_data):
        blog_url = validated_data["url"]
        check = self.blog_exists(blog_url)
        if not check[0]:
            raise serializers.ValidationError(check[1])
        check = Blog.cook_blog(**validated_data) 
        if not check[0]:
            raise serializers.ValidationError(check[1])
        # Update the feed after adding a new blog
        FeedConnector.update_blogs()
        return check[1]


    def to_representation(self, instance):
        data = super().to_representation(instance)
        images = instance.images.all()
        images = [
            {
                "uid" : image.uid,
                "name" : image.name,
                "image_name" : image.image.name,
                "is_published" : image.is_published,
                "created_at" : image.created_at,
                
            } for image in images
        ]
        data['images'] = images
        return data
