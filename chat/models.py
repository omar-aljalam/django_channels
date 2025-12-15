from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, null=True, related_name="sender", editable=False)
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, default=None, related_name="receiver", editable=False)
    date = models.DateTimeField(auto_now_add=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False, editable=False)