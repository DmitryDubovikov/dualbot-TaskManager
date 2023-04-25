from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task
from services.mail import send_assign_notification
from tests.base import TestViewSetBase

from factories import UserFactory, TaskFactory


class TestSendEmail(TestViewSetBase):
    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        executor = UserFactory.create()
        task = TaskFactory.create(executor=executor)

        send_assign_notification(task.id)

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[executor.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task.id)},
            ),
        )
