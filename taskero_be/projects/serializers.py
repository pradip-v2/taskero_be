from rest_framework import serializers

from taskero_be.core.serializers import BaseModelSerializer
from taskero_be.projects.models import Project


class ProjectSerializer(BaseModelSerializer[Project]):
    class Meta:
        model = Project
        fields = serializers.ALL_FIELDS
