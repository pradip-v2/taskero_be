from taskero_be.core.tasks.models import TaskStatus
from taskero_be.users.models import User
from django.db.models import QuerySet, Count, F
from taskero_be.tasks.models import Task

def get_member_wise_workload_queryset(project_id: int) -> QuerySet[User]:
    total_tasks = Task.objects.filter(project_id=project_id).count()
    users: QuerySet[User] = User.objects.filter(assigned_tasks__project_id=project_id)\
            .prefetch_related("assigned_tasks")\
            .annotate(task_count=Count("assigned_tasks"))\
            .annotate(workload=F("task_count") * 100 / total_tasks)\
            .only("id", "name", "email")
    return users

def get_status_wise_task_count_queryset(project_id: int) -> QuerySet[TaskStatus]:
    statuses = TaskStatus.objects.filter(tasks__project_id=project_id)\
        .prefetch_related("tasks")\
        .annotate(task_count=Count("tasks"))\
        .only("id", "title")
    return statuses
