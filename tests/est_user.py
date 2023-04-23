from base import TestViewSetBase
from rest_framework.exceptions import ErrorDetail
from factories import factory, UserFactory


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

    def est_list(self):
        data = self.list()
        assert len(data) == 1
        assert data[0]["username"] == self.login_user_attributes["username"]

    def est_list_unautorized(self):
        data = self.list_unautorized()
        assert data == {
            "detail": ErrorDetail(
                string="Authentication credentials were not provided.",
                code="not_authenticated",
            )
        }

    def est_retrieve(self):
        users = self.list()
        assert len(users) > 0
        id_to_retrieve = users[0]["id"]
        data = self.retrieve(args=str(id_to_retrieve))
        assert data["username"] == self.login_user_attributes["username"]

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

    def est_delete(self):
        users = self.list()
        users_number = len(users)
        assert users_number > 0
        id_to_retrieve = users[0]["id"]
        self.delete(args=str(id_to_retrieve))
