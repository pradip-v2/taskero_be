from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema
from taskero_be.core.decorators import add_created_by
from taskero_be.core.decorators import add_updated_by
from taskero_be.project_members.models import ProjectMember
from taskero_be.projects.models import Project
from taskero_be.projects.serializers import ProjectRelationShortSerializer, ProjectSearchResultsSerializer, ProjectSerializer
from rest_framework.decorators import action

class ProjectViewSet(viewsets.ModelViewSet[Project]):
    queryset = Project.objects.select_related("owner").all()
    serializer_class = ProjectSerializer

    @add_created_by
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if serializer.instance and serializer.instance.owner:
            ProjectMember.objects.create(
                member=serializer.instance.owner,
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

    @extend_schema(
        responses={
            200: ProjectSearchResultsSerializer,
        },
    )
    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ProjectRelationShortSerializer(queryset, many=True)
        return Response({"results": serializer.data})
