from django.db import models
from users.models import *

# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    question = models.TextField(blank=True, null=True)
    topic = models.TextField(blank=True, null=True)
    room_id = models.UUIDField(blank=True,null=True)

    def __str__(self) -> str:
        return f"{self.user.email} - {self.id}"
