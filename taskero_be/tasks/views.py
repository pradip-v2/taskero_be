from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework_extensions.mixins import NestedViewSetMixin

from taskero_be.core.decorators import add_created_by
from taskero_be.core.decorators import add_updated_by
from taskero_be.tasks.models import Task
from taskero_be.tasks.serializers import TaskSerializer


class TaskViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet[Task],
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @add_created_by
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @add_updated_by
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class ProjectTasksViewSet(
    NestedViewSetMixin,
    ListModelMixin,
    viewsets.GenericViewSet[Task],
):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    model = Task
