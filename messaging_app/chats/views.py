from rest_framework import viewsets, status, filters
from .serializers import ConversationSerializer, MessageSerializer
from .models import Conversation, Message
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# Create your views here.
class ConversationViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Conversation.objects.all()

        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                participants_id__first_name__icontains=search_query
            ) | queryset.filter(
                participants_id__last_name__icontains=search_query
            ) | queryset.filter(
                participants_id__email__icontains=search_query
            )

        # --- Manual ordering ---
        ordering = request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        serializer = ConversationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        many = isinstance(request.data, list)
        serializer = ConversationSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        conversation = get_object_or_404(Conversation, pk=pk)
        serializer = Message.objects(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        conversation = get_object_or_404(Conversation, pk=pk)
        serializer = MessageSerializer(conversation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def Delete(self, request, pk=None):
        conversation = get_object_or_404(Conversation, pk=pk)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MessageViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset  = Message.objects.all()

        search_query = request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                message_body__icontains=search_query
            ) | queryset.filter(
                sender_id__first_name__icontains=search_query
            ) | queryset.filter(
                sender_id__last_name__icontains=search_query
            ) | queryset.filter(
                sender_id__email__icontains=search_query
            )

        # --- Manual ordering ---
        ordering = request.query_params.get('ordering')
        if ordering:
            queryset = queryset.order_by(ordering)

        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        many = isinstance(request.data, list)
        serializer = MessageSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        message = get_object_or_404(Message, pk=pk)
        serializer = Message.objects(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        message = get_object_or_404(Message, pk=pk)
        serializer = MessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def Delete(self, request, pk=None):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)