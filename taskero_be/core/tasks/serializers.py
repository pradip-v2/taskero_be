from taskero_be.core.serializers import BaseModelSerializer
from taskero_be.core.tasks.models import TaskStatus


class TaskStatusSerializer(BaseModelSerializer[TaskStatus]):
    class Meta:
        model = TaskStatus
        fields = ["id", "title"]
