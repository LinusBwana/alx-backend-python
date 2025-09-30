from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User, null=True, blank=True, related_name="edited_messages", on_delete=models.SET_NULL
    )
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )

    def __str__(self):
        if self.parent_message:
            return f"Reply by {self.sender} to {self.parent_message.id}: {self.content[:20]}"
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"

    def get_all_replies(self):
        """
        Recursively fetch all replies to this message.
        """
        replies = []
        for reply in self.replies.all().select_related("sender").prefetch_related("replies"):
            replies.append(reply)
            replies.extend(reply.get_all_replies())  # recursion
        return replies