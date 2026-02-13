from taskero_be.core.serializers import BaseModelSerializer
from taskero_be.core.tasks.models import TaskStatus
from rest_framework import serializers


class TaskStatusSerializer(BaseModelSerializer[TaskStatus]):
    class Meta:
        model = TaskStatus
        fields = ["id", "title", "parent_status"]


class StateTransitionSerializer(BaseModelSerializer[TaskStatus]):
    children = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TaskStatus.objects.all())

    class Meta:
        model = TaskStatus
        fields = ["id", "title", "children"]


class StateTransitionsMapSerializer(serializers.Serializer):
    state_transitions_map = serializers.DictField(
        child=StateTransitionSerializer())
