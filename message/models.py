from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="received_messages", on_delete=models.CASCADE
    )
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)  # ✅ 已读/未读状态

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.message[:30]}"
