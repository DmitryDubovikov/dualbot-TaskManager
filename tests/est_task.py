from base import TestViewSetBase
from rest_framework.exceptions import ErrorDetail
from main.models import User, Tag


class TestTaskViewSet(TestViewSetBase):
    basename = "tasks"
    login_user_attributes = {
        "username": "userlogin",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        # "date_of_birth": "2000-01-01",
        # "phone": "+79000000000",
        "role": "developer",
    }

    task_attributes = {
        "id": 1,
        "header": "cool task",
        "description": "this is a cool task",
        "created_at": "2023-02-24T13:45:14.237856Z",
        "updated_at": "2023-02-24T13:45:14.237871Z",
        "deadline": "2023-01-24T13:45:07Z",
        "status": "new task",
        "priority": 2,
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def create_task(self):
        task_attributes = self.task_attributes.copy()
        user = User.objects.all()[0]
        task_attributes["author"] = user.id
        task_attributes["executor"] = user.id
        return self.create(task_attributes)

    def test_create(self):
        task = self.create_task()
        expected_response = self.expected_details(task, self.task_attributes)
        assert task["header"] == expected_response["header"]
        assert task["description"] == expected_response["description"]
        assert task["priority"] == expected_response["priority"]
        assert task["status"] == expected_response["status"]
        assert task["deadline"] == expected_response["deadline"]

    def test_list(self):
        task = self.create_task()
        data = self.list()
        assert len(data) == 1
        expected_response = self.expected_details(task, self.task_attributes)
        assert data[0]["header"] == expected_response["header"]
        assert data[0]["description"] == expected_response["description"]
        assert data[0]["priority"] == expected_response["priority"]
        assert data[0]["status"] == expected_response["status"]
        assert data[0]["deadline"] == expected_response["deadline"]

    def test_list_unautorized(self):
        data = self.list_unautorized()
        assert data == {
            "detail": ErrorDetail(
                string="Authentication credentials were not provided.",
                code="not_authenticated",
            )
        }

    def test_retrieve(self):
        task = self.create_task()
        id_to_retrieve = task["id"]
        data = self.retrieve(args=[str(id_to_retrieve)])
        expected_response = self.expected_details(task, self.task_attributes)
        assert data["header"] == expected_response["header"]
        assert data["description"] == expected_response["description"]
        assert data["priority"] == expected_response["priority"]
        assert data["status"] == expected_response["status"]
        assert data["deadline"] == expected_response["deadline"]

    def test_retrieve_filtered(self):
        task = self.create_task()
        data = self.retrieve_filtered(args=["?status=new"])
        expected_response = self.expected_details(task, self.task_attributes)
        assert data[0]["header"] == expected_response["header"]
        assert data[0]["description"] == expected_response["description"]
        assert data[0]["priority"] == expected_response["priority"]
        assert data[0]["status"] == expected_response["status"]
        assert data[0]["deadline"] == expected_response["deadline"]

    def test_update(self):
        task = self.create_task()
        id_to_retrieve = task["id"]
        data = self.update(args=str(id_to_retrieve), data={"header": "updated"})
        assert data["header"] == "updated"

    def test_delete(self):
        task = self.create_task()
        tasks = self.list()
        tasks_number = len(tasks)
        assert tasks_number > 0
        id_to_retrieve = task["id"]
        self.delete(args=str(id_to_retrieve))
        assert tasks_number - len(self.list()) == 1
