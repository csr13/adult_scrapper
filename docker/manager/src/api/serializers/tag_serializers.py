from rest_framework import serializers

from manager.models import BlogTag


class BlogTagModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogTag
        fields = [
            'pk', 
            'uid', 
            'name', 
            'slug'
        ]
        read_only_fields = [
            'uid', 
            'slug'
        ]


    def create(self, validated_data):
        blog = BlogTag(**validated_data)
        try:
            blog.save()
        except Exception as error:
            raise serializers.ValidationError(
                "Tag %s already exists." % validated_data["name"]
            )
        return blog
