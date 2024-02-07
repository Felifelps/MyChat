from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    STATUS_CHOICES = (
        ('r', 'read'),
        ('s', 'sent')
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='messages_sent'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='messages_receivedt'
    )

    status = models.CharField(max_length=20, default='s', choices=STATUS_CHOICES)

    date = models.DateTimeField(auto_now_add=True)

    text = models.TextField()

    def __str__(self) -> str:
        return f'{self.sender} -> {self.receiver}: {self.text}'
