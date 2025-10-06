from rest_framework import viewsets

from taskero_be.core.decorators import add_created_by
from taskero_be.core.decorators import add_updated_by
from taskero_be.projects.models import Project
from taskero_be.projects.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet[Project]):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @add_created_by
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @add_updated_by
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
