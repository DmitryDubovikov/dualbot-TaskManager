from django.urls import path, include
from rest_framework.routers import SimpleRouter
from main.views import (
    UserViewSet,
    TaskViewSet,
    TagViewSet,
    intentional_error,
    CurrentUserViewSet,
)
from services.single_resource import BulkRouter

# router = SimpleRouter()
router = BulkRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"tags", TagViewSet, basename="tags")

router.register(r"current-user", CurrentUserViewSet, basename="current_user")

urlpatterns = [
    path("api/", include(router.urls)),
    path("error/", intentional_error, name="error"),
]
