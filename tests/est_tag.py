from base import TestViewSetBase
from rest_framework.exceptions import ErrorDetail


class TestTagViewSet(TestViewSetBase):
    basename = "tags"
    login_user_attributes = {
        "username": "userlogin",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        # "date_of_birth": "2000-01-01",
        # "phone": "+79000000000",
        "role": "developer",
    }
    tag_attributes = {"header": "new tag"}

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag = self.create(self.tag_attributes)
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag["header"] == expected_response["header"]

    def test_list(self):
        self.create(self.tag_attributes)
        self.create(self.tag_attributes)
        data = self.list()
        assert len(data) == 2
        tag = data[1]
        expected_response = self.expected_details(tag, self.tag_attributes)
        assert tag["header"] == expected_response["header"]

    def test_list_unautorized(self):
        data = self.list_unautorized()
        assert data == {
            "detail": ErrorDetail(
                string="Authentication credentials were not provided.",
                code="not_authenticated",
            )
        }

    def test_retrieve(self):
        data = self.create(self.tag_attributes)
        id_to_retrieve = data["id"]
        data = self.retrieve(args=[str(id_to_retrieve)])
        assert data["header"] == self.tag_attributes["header"]

    def test_update(self):
        data = self.create(self.tag_attributes)
        id_to_retrieve = data["id"]
        data = self.update(args=str(id_to_retrieve), data={"header": "updated"})
        assert data["header"] == "updated"

    def test_delete(self):
        self.create(self.tag_attributes)
        tags = self.list()
        tags_number = len(tags)
        assert tags_number > 0
        id_to_retrieve = tags[0]["id"]
        self.delete(args=str(id_to_retrieve))
        assert tags_number - len(self.list()) == 1
