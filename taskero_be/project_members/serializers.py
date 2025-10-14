from rest_framework import serializers

from taskero_be.core.serializers import BaseModelSerializer
from taskero_be.project_members.models import ProjectMember
from taskero_be.projects.serializers import ProjectRelationShortSerializer
from taskero_be.users.api.serializers import UserRelationShortSerializer


class ProjectMemberSerializer(BaseModelSerializer[ProjectMember]):
    project_data = ProjectRelationShortSerializer(
        source="project",
        read_only=True,
        default=None,
    )
    member_data = UserRelationShortSerializer(
        source="member",
        read_only=True,
        default=None,
    )

    class Meta:
        model = ProjectMember
        fields = serializers.ALL_FIELDS


class ProjectWiseMember(BaseModelSerializer[ProjectMember]):
    member_data = UserRelationShortSerializer(
        source="member",
        read_only=True,
        allow_null=True,
        default=None,
    )

    class Meta:
        model = ProjectMember
        fields = ["member_data", "created_at"]
