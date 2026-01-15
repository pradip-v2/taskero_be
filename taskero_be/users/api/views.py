from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from taskero_be.users.api.serializers import CurrentUserDetailSerializer
from taskero_be.users.api.serializers import UserProjectSerializer
from taskero_be.users.api.serializers import UserRelationShortSerializer
from taskero_be.users.api.serializers import UserSearchResultsSerializer
from taskero_be.users.api.serializers import UserSerializer
from taskero_be.users.models import User


class UserViewSet(viewsets.ModelViewSet[User]):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: CurrentUserDetailSerializer,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CurrentUserDetailSerializer(instance)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @extend_schema(
        responses={
            200: UserProjectSerializer(many=True),
        },
    )
    @action(detail=True, methods=["get"], url_path="projects")
    def projects(self, request, *args, **kwargs):
        instance = self.get_object()
        projects = instance.project_members.values(
            "project__title",
            "project__id",
            "project__owner__name",
        )
        page = self.paginate_queryset(projects)
        if page is not None:
            return self.get_paginated_response(page)

        return Response(status=status.HTTP_200_OK, data=page)

    @extend_schema(
        responses={
            200: UserSearchResultsSerializer,
        },
        parameters=[
            OpenApiParameter(
                name="q",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search query for user names",
            ),
        ],
    )
    @action(detail=False, methods=["get"], url_path="search")
    def search(self, request, *args, **kwargs):
        query = request.query_params.get("q", "")
        queryset = self.get_queryset().filter(name__icontains=query)
        serializer = UserRelationShortSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data={"results": serializer.data})
