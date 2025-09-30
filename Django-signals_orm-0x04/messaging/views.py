from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    """
    Allows a logged-in user to delete their account.
    """
    user = request.user
    user.delete()  # This triggers the post_delete signal
    return redirect("home")  # Redirect to homepage after deletion
