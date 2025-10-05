from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer, 
    MessageSerializer, 
)
from .permissions import IsParticipantOfConversation, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['participants', 'created_at']
    search_fields = ['participants__username', 'participants__email']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Filter conversations by participant if user_id is provided."""
         # Only return conversations where the current user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        """Automatically add the current user as a participant when creating a conversation."""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
    
    # not sure of this function
    def remove_participant(self, request, pk=None):
        """Remove a participant from a conversation."""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_403_FORBIDDEN
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
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sender', 'conversation', 'sent_at']
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']
    
    def get_queryset(self):
        """Filter messages to only show those the user has access to."""
        # Return messages where the user is either the sender or a participant in the conversation
        return Message.objects.filter(
            models.Q(sender=self.request.user) | 
            models.Q(conversation__participants=self.request.user)).distinct()
    
    def perform_create(self, serializer):
        """Automatically set the sender to the current user when creating a message."""
        serializer.save(sender=self.request.user)