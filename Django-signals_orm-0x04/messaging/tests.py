from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class MessagingSignalTests(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='password123')
        self.receiver = User.objects.create_user(username='bob', password='password123')

    def test_notification_created_on_message_send(self):
        """
        Ensure that when a message is sent, a notification is automatically created for the receiver.
        """
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello Bob!"
        )

        # Check that the notification exists
        notification = Notification.objects.filter(user=self.receiver, message=message).first()
        self.assertIsNotNone(notification)
        self.assertFalse(notification.is_read)
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
