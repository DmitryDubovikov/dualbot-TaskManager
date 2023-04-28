from factory.django import DjangoModelFactory
import factory
from faker import Faker
from django.core.files.uploadedfile import SimpleUploadedFile
from faker.providers import BaseProvider
from main.models import User, Task


class ImageFileProvider(BaseProvider):
    def image_file(self, fmt: str = "jpeg") -> SimpleUploadedFile:
        return SimpleUploadedFile(
            self.generator.file_name(extension=fmt),
            self.generator.image(image_format=fmt),
        )


fake = Faker()
fake.add_provider(ImageFileProvider)


class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    password = factory.PostGenerationMethodCall("set_password", "password")
    avatar_picture = factory.LazyAttribute(lambda _: fake.unique.image_file("jpeg"))

    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    email = factory.LazyAttribute(lambda _: fake.unique.email())
    role = factory.LazyAttribute(
        lambda _: fake.word(
            ext_word_list=[
                "developer",
                "manager",
                "admin",
            ]
        )
    )

    class Meta:
        model = User


class TaskFactory(DjangoModelFactory):
    header = factory.LazyAttribute(lambda _: factory.Faker("text", max_nb_chars=100))
    description = factory.LazyAttribute(
        lambda _: factory.Faker("text", max_nb_chars=100)
    )

    class Meta:
        model = Task
