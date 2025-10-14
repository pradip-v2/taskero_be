from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework_extensions.mixins import NestedViewSetMixin

from taskero_be.project_members.models import ProjectMember
from taskero_be.project_members.serializers import ProjectMemberSerializer
from taskero_be.project_members.serializers import ProjectWiseMember


class ProjectMemberViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer


class ProjectWiseProjectMemberViewSet(
    NestedViewSetMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet[ProjectMember],
):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectWiseMember
    model = ProjectMember
    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    filterset_fields = {
        "member__name": ["icontains"],
        "member__email": ["icontains"],
        "member__id": ["exact"],
    }
    search_fields = ["member__name"]
