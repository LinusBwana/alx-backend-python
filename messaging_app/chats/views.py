from rest_framework import viewsets, filters, status, mixins
from .serializers import ConversationSerializer, MessageSerializer, CustomUserSerializer, LoginSerializer
from .models import Conversation, Message
from rest_framework import serializers
from . models import CustomUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsParticipantOfConversation, CanAccessMessagesInUserConversations, CanOnlyEditOwnMessages
from .auth import CustomJWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from .pagination import CustomMessagePagination
from rest_framework.exceptions import PermissionDenied


# Create your views here.
class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class LoginViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Handle user login (POST request)
        """
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            # Valid login, returning access and refresh tokens
            user = serializer.validated_data['user']
            user_data = CustomUserSerializer(user).data
            return Response({
                'refresh': serializer.validated_data['refresh'],
                'access': serializer.validated_data['access'],
                'user': user_data
            }, status=status.HTTP_200_OK)

        # If invalid login credentials
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    authentication_classes = [CustomJWTAuthentication]
    
    # Enable filtering, searching, and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants_id__first_name', 'participants_id__last_name', 'participants_id__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants_id=user).distinct()

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [CanAccessMessagesInUserConversations, CanOnlyEditOwnMessages]
    authentication_classes = [CustomJWTAuthentication]
    pagination_class = CustomMessagePagination

     # Enable filtering, searching, and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender_id__first_name', 'sender_id__last_name']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at'] 

    def get_queryset(self):
        """Filter messages by conversation when accessed through nested route"""
        conversation_pk = self.kwargs.get('conversation_pk')
        user = self.request.user

        if conversation_pk:
            # Check if user has access to this conversation
            if not Conversation.objects.filter(pk=conversation_pk, participants_id=user).exists():
                raise PermissionDenied("You don't have permission to access this conversation")
            return Message.objects.filter(conversation_id=conversation_pk, conversation__participants_id=user)
        return Message.objects.filter(conversation__participants_id=user)

    def perform_create(self, serializer):
        """Automatically set the conversation when creating a message through nested route"""
        conversation_pk = self.kwargs.get('conversation_pk')

        if conversation_pk:
            try:
                conversation = Conversation.objects.get(pk=conversation_pk)
                # Check if user is participant of the conversation
                if not conversation.participants_id.filter(user_id=self.request.user.user_id).exists():
                    raise PermissionDenied("You don't have permission to post messages in this conversation")
                serializer.save(conversation=conversation, sender_id=self.request.user)
            except Conversation.DoesNotExist:
                raise serializers.ValidationError("Conversation not found")
        else:
            serializer.save(sender_id=self.request.user)