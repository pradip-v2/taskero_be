from django.db.models import Count
from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
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
    queryset = Task.objects.all().annotate(subtasks_count=Count("subtasks"))
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
    queryset = Task.objects.all().annotate(subtasks_count=Count("subtasks"))
    serializer_class = TaskSerializer
    model = Task
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        "title": ["icontains"],
        "level": ["exact"],
        "is_done": ["exact"],
        "status": ["exact"],
        "created_by": ["exact"],
        "updated_by": ["exact"],
        "created_at": ["exact", "gte", "lte"],
        "updated_at": ["exact", "gte", "lte"],
        "parent_task": ["exact"],
        "description": ["icontains"],
    }
    search_fields = ["title", "description"]
