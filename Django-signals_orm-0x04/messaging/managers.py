from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager that returns unread messages for a given user.
    The view can further limit fields with .only(...) if desired.
    """
    def unread_for_user(self, user):
        """
        Return a QuerySet of unread messages for `user`.
        We select_related('sender') here to avoid N+1 when accessing sender.
        """
        return (
            super()
            .get_queryset()
            .filter(receiver=user, read=False)
            .select_related('sender')
        )
