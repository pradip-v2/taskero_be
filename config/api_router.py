from rest_framework_extensions.routers import ExtendedSimpleRouter

from taskero_be.projects.views import ProjectViewSet
from taskero_be.tasks.views import ProjectTasksViewSet
from taskero_be.tasks.views import TaskViewSet
from taskero_be.users.api.views import UserViewSet

router = ExtendedSimpleRouter()


router.register("users", UserViewSet)
router.register(
    "projects",
    ProjectViewSet,
    basename="projects",
).register(
    "tasks",
    ProjectTasksViewSet,
    basename="project_tasks",
    parents_query_lookups=["project"],
)
router.register("tasks", TaskViewSet, basename="tasks")


app_name = "api"
urlpatterns = router.urls
