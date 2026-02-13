from drf_spectacular.utils import extend_schema

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from taskero_be.core.tasks.models import TaskStatus
from taskero_be.core.tasks.serializers import StateTransitionSerializer, StateTransitionsMapSerializer, TaskStatusSerializer


class TaskStatusViewSet(
    viewsets.ModelViewSet[TaskStatus]
):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer
    pagination_class = None

    @extend_schema(responses={200: StateTransitionsMapSerializer})
    @action(detail=False, methods=["get"], url_path="task-status-workflow")
    def task_status_workflow(self, request, *args, **kwargs):
        statuses = TaskStatus.objects.prefetch_related("children").all()
        state_transitions_map = {
            str(status.pk): StateTransitionSerializer(status).data
            for status in statuses
        }
        return Response({"state_transitions_map": state_transitions_map})
