from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Friendship(models.Model):
    STATUS_CHOICES = (
        ('w', 'waiting'),
        ('a','accepted'),
        ('r', 'rejected')
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='friendship_sent'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        related_name='friendship_received'
    )
    status = models.CharField(max_length=20, default='w', choices=STATUS_CHOICES)
    date = models.DateField(auto_now_add=True)

class Token(models.Model):
    token = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"<Token {self.token}>"