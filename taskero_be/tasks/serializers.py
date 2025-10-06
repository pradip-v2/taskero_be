from rest_framework import serializers

from taskero_be.core.serializers import BaseModelSerializer
from taskero_be.tasks.models import Task


class TaskSerializer(BaseModelSerializer[Task]):
    class Meta:
        model = Task
        fields = serializers.ALL_FIELDS
