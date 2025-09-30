import uuid
from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager

User = get_user_model()


class Message(models.Model):
    """
    Represents a message sent from one user to another.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Unread/read state for inbox filtering
    read = models.BooleanField(default=False)

    # Edit tracking
    edited = models.BooleanField(default=False)  # Track if the message has been edited

    # track who made the edit
    edited_by = models.ForeignKey(User, related_name="edited_messages",
        null=True, blank=True, on_delete=models.SET_NULL
    )

    # self-referential FK for threaded replies
    parent_message = models.ForeignKey("self", null=True, blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )

    # Managers
    objects = models.Manager()  # default
    unread = UnreadMessagesManager()  # custom manager

    def __str__(self):
        if self.parent_message:
            return f"Reply by {self.sender} to msg-{self.parent_message.id}: {self.content[:20]}"
        return f"From {self.sender.username} to {self.receiver.username}: {self.content[:20]}"

    def get_all_replies(self):
        """
        Recursively fetch all replies to this message.
        """
        replies = []
        for reply in self.replies.all().select_related("sender").prefetch_related("replies"):
            replies.append(reply)
            replies.extend(reply.get_all_replies())
        return replies
    

class Notification(models.Model):
    """
    Stores notifications generated when a user receives a new message.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID {self.message.id}"
    

class MessageHistory(models.Model):
    """
    Stores old versions of a message whenever it is edited.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    # track who made the edit
    edited_by = models.ForeignKey(User, related_name="message_edits",
        null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"History of message {self.message.id} at {self.edited_at}"
    