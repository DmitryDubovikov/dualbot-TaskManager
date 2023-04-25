from rest_framework import serializers
from django.core.files.base import File
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from .models import User, Task, Tag
from task_manager import settings


class FileMaxSizeValidator:
    def __init__(self, max_size: int) -> None:
        self.max_size = max_size

    def __call__(self, value: File) -> None:
        if value.size > self.max_size:
            raise ValidationError(f"Maximum size {self.max_size} exceeded.")


class UserSerializer(serializers.ModelSerializer):
    avatar_picture = serializers.FileField(
        required=False,
        validators=[
            FileMaxSizeValidator(settings.UPLOAD_MAX_SIZES["avatar_picture"]),
            FileExtensionValidator(["jpeg", "jpg", "png"]),
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            # "date_of_birth",
            # "phone",
            "role",
            "avatar_picture",
        )


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    executor = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "header",
            "description",
            "created_at",
            "updated_at",
            "deadline",
            "status",
            "priority",
            "author",
            "executor",
            "tags",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "header", "uid")
