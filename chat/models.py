from django.db import models


class Message(models.Model):
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE)
    receiver = models.ForeignKey('users.User', on_delete=models.CASCADE)
    text = models.TextField()

