from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Signal to create a notification when a new message is sent.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log the old content of a message before it is updated.
    Triggered only if the message already exists and content is being changed.
    """
    if not instance.pk:
        # Skip if this is a new message
        return

    try:
        # Get the current version from the database
        existing_message = Message.objects.get(pk=instance.pk)

        # Check if the content is different
        if existing_message.content != instance.content:
            # Save old content to MessageHistory
            MessageHistory.objects.create(
                message=existing_message,
                old_content=existing_message.content
            )

            # Mark the message as edited
            instance.edited = True

    except Message.DoesNotExist:
        # In case the message is new or doesn't exist in the DB
        pass


@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """
    When a User is deleted, clean up all related messages, notifications, and histories.
    """
    # Delete all messages sent or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete all histories edited by the user
    MessageHistory.objects.filter(edited_by=instance).delete()