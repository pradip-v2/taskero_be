from rest_framework import mixins
from rest_framework import viewsets

from taskero_be.core.tasks.models import TaskStatus
from taskero_be.core.tasks.serializers import TaskStatusSerializer


class TaskStatusViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    pagination_class = None
