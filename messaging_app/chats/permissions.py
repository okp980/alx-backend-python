from rest_framework.permissions import BasePermission
from chats.models import Conversation
from rest_framework import permissions


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation.
        """
        return request.user in obj.participants.all()
    
class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed for any request,
        so we'll always allow GET, HEAD or OPTIONS requests.
        """
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return True
        """
        Check if the user is the owner of the object.
        """
        return request.user == obj.sender