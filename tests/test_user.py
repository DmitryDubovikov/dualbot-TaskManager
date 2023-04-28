from base import TestViewSetBase
from rest_framework.exceptions import ErrorDetail
from django.forms.models import model_to_dict
from django.core.files.uploadedfile import SimpleUploadedFile
from factories import factory, UserFactory
from http import HTTPStatus


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
        }

    def test_create(self):
        user_attributes = model_to_dict(
            UserFactory.build(),
            fields=[
                "username",
                "avatar_picture",
                "first_name",
                "last_name",
                "email",
                "role",
            ],
        )
        user = self.create(user_attributes)
        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

    def test_list(self):
        user_attributes = model_to_dict(
            UserFactory.build(),
            fields=[
                "username",
                "avatar_picture",
                "first_name",
                "last_name",
                "email",
                "role",
            ],
        )
        user = self.create(user_attributes)
        expected_response = self.expected_details(user, user_attributes)

        data = self.list()
        assert len(data) == 2
        assert data[1] == expected_response

    def test_list_unautorized(self):
        data = self.list_unautorized()
        assert data == {
            "detail": ErrorDetail(
                string="Authentication credentials were not provided.",
                code="not_authenticated",
            )
        }

    # TODO: во-первых, какая-то многословная схема с созданием user_attributes и не DRY!
    # во-вторых,  Not Found: /api/users/1/
    def est_retrieve(self):
        user_attributes = model_to_dict(
            UserFactory.build(),
            fields=[
                "username",
                "avatar_picture",
                "first_name",
                "last_name",
                "email",
                "role",
            ],
        )
        user = self.create(user_attributes)
        expected_response = self.expected_details(user, user_attributes)
        users = self.list()

        assert len(users) == 2
        id_to_retrieve = users[1]["id"]
        data = self.retrieve(args=str(id_to_retrieve))
        assert data == expected_response

    def est_update(self):
        users = self.list()
        assert len(users) > 0
        id_to_retrieve = users[0]["id"]
        data = self.update(
            args=str(id_to_retrieve),
            data={"username": "updated", "first_name": "updated"},
        )
        assert data["username"] == "updated"
        assert data["first_name"] == "updated"

    def test_delete(self):
        users = self.list()
        users_number = len(users)
        assert users_number > 0
        id_to_retrieve = users[0]["id"]
        self.delete(args=str(id_to_retrieve))

    def test_large_avatar(self) -> None:
        self.client.force_authenticate(self.user)
        user_attributes = model_to_dict(
            UserFactory.build(
                avatar_picture=SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
            ),
            fields=[
                "username",
                "avatar_picture",
                "first_name",
                "last_name",
                "email",
                "role",
            ],
        )
        response = self.client.post(self.list_url(), data=user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        self.client.force_authenticate(self.user)
        user_attributes = model_to_dict(
            UserFactory.build(),
            fields=[
                "username",
                "avatar_picture",
                "first_name",
                "last_name",
                "email",
                "role",
            ],
        )
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.client.post(self.list_url(), data=user_attributes)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }
