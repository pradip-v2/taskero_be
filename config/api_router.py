from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from taskero_be.projects.views import ProjectViewSet
from taskero_be.tasks.views import TaskViewSet
from taskero_be.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("projects", ProjectViewSet, basename="projects")
router.register("tasks", TaskViewSet, basename="tasks")


app_name = "api"
urlpatterns = router.urls
