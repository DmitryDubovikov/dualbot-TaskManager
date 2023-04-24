from factory.django import DjangoModelFactory
import factory

from main.models import User, Task


class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User


class TaskFactory(DjangoModelFactory):
    header = factory.LazyAttribute(lambda _: factory.Faker("text", max_nb_chars=100))
    description = factory.LazyAttribute(
        lambda _: factory.Faker("text", max_nb_chars=100)
    )

    class Meta:
        model = Task
