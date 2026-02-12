from rest_framework import serializers

from taskero_be.core.serializers import BaseModelSerializer
from taskero_be.projects.models import Project
from taskero_be.users.api.serializers import UserRelationShortSerializer


class ProjectSerializer(BaseModelSerializer[Project]):
    owner_data = UserRelationShortSerializer(source="owner", read_only=True)

    class Meta:
        model = Project
        fields = serializers.ALL_FIELDS


class ProjectRelationShortSerializer(BaseModelSerializer[Project]):
    owner_data = UserRelationShortSerializer(
        source="owner",
        read_only=True,
        default=None,
    )

    class Meta:
        model = Project
        fields = ["id", "title", "owner_data"]

class ProjectSearchResultsSerializer(serializers.Serializer):
    results = ProjectRelationShortSerializer(many=True)
