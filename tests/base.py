from typing import Union, List
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from main.models import User


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user(cls.login_user_attributes)
        cls.client = APIClient()

    @staticmethod
    def create_api_user(login_user_attributes):
        return User.objects.create(**login_user_attributes)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == 201, response.content
        return response.data

    def list(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(args))
        assert response.status_code == 200
        return response.data

    def list_unautorized(self, args: List[Union[str, int]] = None) -> dict:
        response = self.client.get(self.list_url(args))
        assert response.status_code == 403
        return response.data

    def retrieve(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(key=args[0]))
        assert response.status_code == 200
        return response.data

    def retrieve_filtered(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        url = self.detail_url(key=args[0])[:-1]
        url = url.replace("%3F", "?")
        response = self.client.get(url)
        assert response.status_code == 200
        return response.data

    def update(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.patch(self.detail_url(key=args), data=data)
        assert response.status_code == 200
        return response.data

    def delete(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.delete(self.detail_url(key=args))
        assert response.status_code == 204
        return response.data
