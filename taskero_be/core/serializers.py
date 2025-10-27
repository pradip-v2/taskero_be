from rest_framework import serializers

from taskero_be.core.models import BaseModel
from taskero_be.users.models import User


class UserMinDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")


class BaseModelSerializer[T](serializers.ModelSerializer[T]):
    """
    Base serializer for all models.
    """

    created_by_data = UserMinDetailsSerializer(
        source="created_by",
        read_only=True,
        required=False,
        default=None,
        allow_null=True,
    )
    updated_by_data = UserMinDetailsSerializer(
        source="updated_by",
        read_only=True,
        required=False,
        default=None,
        allow_null=True,
    )

    class Meta:
        model = BaseModel
        fields = serializers.ALL_FIELDS
        abstract = True


class ResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class GeneratePresignedURLRequestSerializer(serializers.Serializer):
    filename = serializers.CharField()
    content_type = serializers.CharField()


class GeneratePresignedURLResponseSerializer(serializers.Serializer):
    upload_url = serializers.CharField()
    file_url = serializers.CharField()
    key = serializers.CharField()
