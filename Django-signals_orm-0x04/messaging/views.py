from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

User = get_user_model()

@cache_page(60)
@login_required
def delete_user(request):
    """
    Allows a logged-in user to delete their account.
    """
    user = request.user
    user.delete()  # This triggers the post_delete signal
    return redirect("home")  # Redirect to homepage after deletion


@cache_page(60)
@login_required
def conversation_view(request, user_id):
    """
    Fetch all messages between the logged-in user and another user,
    with threaded replies. Optimized with select_related, prefetch_related, and .only().
    """
    other_user = get_object_or_404(User, pk=user_id)

    messages = (
        Message.objects.filter(
            sender=request.user, receiver=other_user
        ) | Message.objects.filter(
            sender=other_user, receiver=request.user
        )
    ).select_related("sender", "receiver", "parent_message") \
     .prefetch_related("replies__sender") \
     .only("id", "sender", "receiver", "content", "timestamp", "parent_message") \
     .order_by("timestamp")

    return render(request, "messaging/conversation.html", {
        "messages": messages,
        "other_user": other_user
    })


@cache_page(60)
@login_required
def inbox_view(request):
    """
    Display only unread messages for the logged-in user.
    Optimized with .only() to fetch only required fields.
    """
    unread_messages = (
        Message.unread.unread_for_user(request.user)
        .only("id", "sender", "content", "timestamp")
    )

    return render(request, "messaging/inbox.html", {
        "unread_messages": unread_messages
    })