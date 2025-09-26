from rest_framework.permissions import BasePermission
from .models import Conversation, Message
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """
    Simple rule: Users can only see conversations they are part of
    """
    def has_permission(self, request, view):
        # Step 1: Check if user is logged in
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Step 2: Check if this conversation belongs to this user
        # obj is the conversation we're trying to access
        if not isinstance(obj, Conversation):
            return False
        
        # Everyone can view if they are the participant
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return obj.participants_id == request.user
        
        # Only the participant can modify or delete
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.participants_id == request.user
        
        return False


class CanAccessMessagesInUserConversations(BasePermission):
    """
    Allows access only to messages that belong to conversations 
    the requesting user is a participant of.
    """
    def has_permission(self, request, view):
        # Step 1: Check if user is logged in
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Step 2: Check if this message is in a conversation the user is part of
        # obj is the message we're trying to access
        if isinstance(obj, Message):
            return obj.conversation.participants_id == request.user
        return False


class CanOnlyEditOwnMessages(BasePermission):
    """
    Simple rule: Users can only edit/delete their own messages
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if not isinstance(obj, Message):
            return False
        
        # For viewing: check if user is in the conversation
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return obj.conversation.participants_id == request.user
        
        # For editing/deleting: must be the person who sent the message
        return obj.sender_id == request.user