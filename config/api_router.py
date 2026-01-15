from rest_framework_extensions.routers import ExtendedSimpleRouter

from taskero_be.communication.views import ConversationMessagesViewSet
from taskero_be.communication.views import ConversationViewSet
from taskero_be.communication.views import MessageViewSet
from taskero_be.core.tasks.views import TaskStatusViewSet
from taskero_be.project_members.views import ProjectMemberViewSet
from taskero_be.project_members.views import ProjectWiseProjectMemberViewSet
from taskero_be.projects.views import ProjectViewSet
from taskero_be.tasks.views import ProjectTasksViewSet
from taskero_be.tasks.views import TaskViewSet
from taskero_be.tenants.views import TenantViewSet
from taskero_be.users.api.views import UserViewSet

router = ExtendedSimpleRouter()


router.register("users", UserViewSet)

projects_router = router.register(
    "projects",
    ProjectViewSet,
    basename="projects",
)
projects_router.register(
    "tasks",
    ProjectTasksViewSet,
    basename="project_tasks",
    parents_query_lookups=["project"],
)
router.register("task-status", TaskStatusViewSet, basename="task_status")
projects_router.register(
    "project-wise-project-members",
    ProjectWiseProjectMemberViewSet,
    basename="project_wise_project_members",
    parents_query_lookups=["project"],
)

router.register("project-members", ProjectMemberViewSet, basename="project_members")
router.register("tasks", TaskViewSet, basename="tasks")
router.register("tenants", TenantViewSet, basename="tenants")

# Communication app routers
conversation_router = router.register(
    "conversations",
    ConversationViewSet,
    basename="conversations",
)
conversation_router.register(
    "messages",
    ConversationMessagesViewSet,
    basename="conversation-messages",
    parents_query_lookups=["conversation"],
)
router.register("messages", MessageViewSet, basename="messages")


app_name = "api"
urlpatterns = router.urls
