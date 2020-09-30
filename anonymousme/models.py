from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Message(models.Model):
    message = models.TextField(blank=False, null=False, max_length=350)
    timestamp = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return f" {self.message} {self.timestamp}"

    def serialize(self):
        return {
            'id' : self.id,
            'message' : self.message,
            'timestamp' : self.timestamp.strftime("%b %#d %Y, %#I:%M %p")
        }

class User(AbstractUser):
    message = models.ManyToManyField(Message, blank=True, related_name='posts')

    def serialize(self):
        return {
            'id' : self.id,
            'person' : self.username,
            'message' : [message.message for message in self.message.all()],
            'timestamp' : [message.timestamp.strftime("%b %#d %Y, %#I:%M %p") for message in self.message.all()],
            'counter' : self.message.count()
        }