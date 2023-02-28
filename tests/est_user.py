from base import TestViewSetBase
from rest_framework.exceptions import ErrorDetail


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmith",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        # "date_of_birth": "2000-01-01",
        # "phone": "+79000000000",
        "role": "developer",
    }
    login_user_attributes = {
        "username": "userlogin",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        # "date_of_birth": "2000-01-01",
        # "phone": "+79000000000",
        "role": "developer",
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_list(self):
        data = self.list()
        assert len(data) == 1
        assert data[0]["username"] == self.login_user_attributes["username"]

    def test_list_unautorized(self):
        data = self.list_unautorized()
        assert data == {
            "detail": ErrorDetail(
                string="Authentication credentials were not provided.",
                code="not_authenticated",
            )
        }

    def test_retrieve(self):
        users = self.list()
        assert len(users) > 0
        id_to_retrieve = users[0]["id"]
        data = self.retrieve(args=str(id_to_retrieve))
        assert data["username"] == self.login_user_attributes["username"]

    def test_update(self):
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
