from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer, 
    MessageSerializer, 
)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['participants', 'created_at']
    search_fields = ['participants__username', 'participants__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter conversations by participant if user_id is provided."""
        queryset = Conversation.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        
        if user_id:
            queryset = queryset.filter(participants__user_id=user_id)
        
        return queryset

    def perform_create(self, serializer):
        """Automatically add the current user as a participant when creating a conversation."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
    
    def remove_participant(self, request, pk=None):
        """Remove a participant from a conversation."""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.remove(user)
            return Response({'message': 'Participant removed successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sender', 'conversation', 'sent_at']
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    
    def get_queryset(self):
        """Filter messages by user ID or conversation ID if provided in query parameters."""
        queryset = Message.objects.all()
        user_pk = self.kwargs.get('user')
        conversation_id = self.request.query_params.get('conversation_id', None)
        
        if user_pk:
            queryset = queryset.filter(sender__user_id=user_pk)
        
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        
        return queryset
    
    def perform_create(self, serializer):
        """Automatically set the sender to the current user when creating a message."""
        serializer.save(sender=self.request.user)