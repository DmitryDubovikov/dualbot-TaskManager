import django_filters
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets

from .models import User, Task, Tag
from .serializers import UserSerializer, TaskSerializer, TagSerializer


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskFilter(django_filters.FilterSet):

    status = django_filters.CharFilter(lookup_expr="icontains")
    author = django_filters.CharFilter(
        field_name="author__username", lookup_expr="icontains"
    )
    executor = django_filters.CharFilter(
        field_name="executor__username", lookup_expr="icontains"
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name="tags__header",
        to_field_name="header",
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Task
        fields = (
            "status",
            "author",
            "executor",
            "tags",
        )


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "executor").prefetch_related("tags").all()
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


def intentional_error(request):
    a = None
    a.hello()  # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")
