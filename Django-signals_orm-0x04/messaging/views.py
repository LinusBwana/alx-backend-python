from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def delete_user(request):
    """
    Allows a logged-in user to delete their account.
    """
    user = request.user
    user.delete()  # This triggers the post_delete signal
    return redirect("home")  # Redirect to homepage after deletion


@login_required
def conversation_view(request, user_id):
    """
    Fetch all messages between the logged-in user and another user,
    with threaded replies. Optimized with select_related + prefetch_related.
    """
    other_user = User.objects.get(pk=user_id)

    messages = (
        Message.objects.filter(
            # 👇 only messages between request.user and the other user
            sender=request.user, receiver=other_user
        ) | Message.objects.filter(
            sender=other_user, receiver=request.user
        )
    ).select_related("sender", "receiver", "parent_message").prefetch_related("replies__sender").order_by("timestamp")

    return render(request, "messaging/conversation.html", {
        "messages": messages,
        "other_user": other_user
    })