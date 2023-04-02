from django.urls import path, include
from rest_framework.routers import SimpleRouter
from main.views import UserViewSet, TaskViewSet, TagViewSet, intentional_error

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"tags", TagViewSet, basename="tags")

urlpatterns = [
    path("api/", include(router.urls)),
    path("error/", intentional_error, name="error"),
]
