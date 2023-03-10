import uuid
from django.db import models


class Tag(models.Model):
    header = models.CharField(max_length=255)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return self.header
