from tests.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "current_user"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def est_retrieve(self):
        self.client.force_authenticate(self.user)
        user = self.single_resource()

        assert user == {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "role": self.user.role,
            "username": self.user.username,
        }

    def test_patch(self):
        self.client.force_authenticate(self.user)
        self.patch_single_resource({"first_name": "TestName"})

        user = self.single_resource()
        assert user["first_name"] == "TestName"
