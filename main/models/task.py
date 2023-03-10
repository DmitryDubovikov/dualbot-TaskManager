from django.db import models
from .user import User
from .tag import Tag


class Task(models.Model):
    class Status(models.TextChoices):
        NEW_TASK = "new task"
        IN_DEVELOPMENT = "in development"
        IN_QA = "in qa"
        IN_CODE_REVIEW = "in_code review"
        READY_FOR_RELEASE = "ready for_release"
        RELEASED = "released"
        ARCHIVED = "archived"

    class Priority(models.IntegerChoices):
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    header = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=100, default=Status.NEW_TASK, choices=Status.choices
    )
    priority = models.IntegerField(choices=Priority.choices, null=True)
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="task_author", null=True
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="task_executor", null=True
    )
    tags = models.ManyToManyField(Tag)

    def __str__(self) -> str:
        return self.header
