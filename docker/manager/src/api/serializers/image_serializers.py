from rest_framework import serializers

from manager.models import Blog, DirtyImage


class ImageSerializer(serializers.ModelSerializer):
    blog_uid = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = DirtyImage
        fields = [
            'pk', 
            'uid', 
            'name', 
            'blog_uid', 
            'image', 
            'is_published'
        ]
        read_only_fields = [
            'is_published', 
            'uid', 
            'pk',
            'parent_blog'
        ]


    def create(self, validated_data):
        name = validated_data["name"]
        blog_uid = validated_data["blog_uid"]
        image = validated_data["image"]
        try:
            image = DirtyImage.objects.get(name=name)
        except DirtyImage.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError("Image exists")
        try:
            blog = Blog.objects.get(uid=blog_uid)
        except Blog.DoesNotExist as error:
            raise serializers.ValidationError("Invalid blog UID")
        image = DirtyImage(
            name=name, 
            image=image, 
            parent_blog=blog
        )
        image.save()
        blog.images.add(image)
        return image


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["image_name"] = instance.image.name
        return data
