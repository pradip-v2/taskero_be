from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from taskero_be.core.decorators import add_created_by
from taskero_be.core.decorators import add_updated_by
from taskero_be.project_members.models import ProjectMember
from taskero_be.projects.models import Project
from taskero_be.projects.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet[Project]):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @add_created_by
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if serializer.instance and serializer.instance.owner:
            ProjectMember.objects.create(
                user=serializer.instance.owner,
                project=serializer.instance,
            )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @add_updated_by
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
