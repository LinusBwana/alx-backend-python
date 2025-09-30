from django.contrib import admin
from .models import Message, Notification, MessageHistory
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'timestamp')
    list_filter = ('timestamp', 'sender', 'receiver')
    search_fields = ('content', 'sender__username', 'receiver__username')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'user')
    search_fields = ('user__username',)


class UserDeletionSignalTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alice", password="pass")
        self.user2 = User.objects.create_user(username="bob", password="pass")
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello Bob!")
        self.notification = Notification.objects.create(user=self.user2, message=self.message)
        self.history = MessageHistory.objects.create(message=self.message, old_content="Old text", edited_by=self.user1)

    def test_user_deletion_cleans_related_data(self):
        self.user1.delete()
        self.assertFalse(Message.objects.filter(sender=self.user1).exists())
        self.assertFalse(Notification.objects.filter(user=self.user1).exists())
        self.assertFalse(MessageHistory.objects.filter(edited_by=self.user1).exists())
