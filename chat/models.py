from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)


class MessageAttachment(models.Model):
    message = models.ForeignKey(
        'chat.Message', on_delete=models.CASCADE, related_name='attachments'
    )
    file = models.FileField(
        upload_to='message_files'
    )
