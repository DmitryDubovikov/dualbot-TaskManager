from factory.django import DjangoModelFactory
import factory

from main.models import User


class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User
