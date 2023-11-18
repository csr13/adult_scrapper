from rest_framework import serializers


class ModelUidSerializer(serializers.Serializer):
    model_uid = serializers.UUIDField(
        required=True,
        format='hex',
        help_text="Any model uid field, uid must be hex."
    )


class ItemExistsResponseSerializer(serializers.Serializer):
    exists = serializers.BooleanField(
        default=False,
        help_text="Whether the requested object exists, without returning the object"
    )
