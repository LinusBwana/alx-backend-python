from rest_framework import viewsets, filters, status
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message


# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    
    # Enable filtering, searching, and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants_id__first_name', 'participants_id__last_name', 'participants_id__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

     # Enable filtering, searching, and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender_id__first_name', 'sender_id__last_name']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at'] 