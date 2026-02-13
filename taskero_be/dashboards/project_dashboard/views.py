from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.decorators import action
from taskero_be.dashboards.project_dashboard.services import get_member_wise_workload_queryset, get_status_wise_task_count_queryset
from taskero_be.dashboards.project_dashboard.serializers import MemberWiseWorkloadSerializer, StatusWiseTaskCountSerializer


class ProjectDashboardViewSet(viewsets.GenericViewSet):
    pagination_class = None
    
    @extend_schema(
        parameters=[
            OpenApiParameter("project_id", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: MemberWiseWorkloadSerializer(many=True),
        },
    )
    @action(detail=False, methods=["get"], url_path="member-wise-workload")
    def member_wise_workload(self, request, *args, **kwargs):
        project_id = request.query_params.get("project_id")
        queryset = get_member_wise_workload_queryset(project_id)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = MemberWiseWorkloadSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = MemberWiseWorkloadSerializer(queryset, many=True)

        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter("project_id", OpenApiTypes.INT,
                             OpenApiParameter.QUERY),
        ],
        responses={
            200: StatusWiseTaskCountSerializer(many=True),
        },
    )
    @action(detail=False, methods=["get"], url_path="status-wise-task-count")
    def status_wise_task_count(self, request, *args, **kwargs):
        project_id = request.query_params.get("project_id")
        queryset = get_status_wise_task_count_queryset(project_id)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = StatusWiseTaskCountSerializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StatusWiseTaskCountSerializer(queryset, many=True)

        return Response(serializer.data)