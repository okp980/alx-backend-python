from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'url', 'user_id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'created_at'
        ]
        read_only_fields = ['user_id', 'created_at']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }

class MessageSerializer(serializers.HyperlinkedModelSerializer):
    sender = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all(),
        lookup_field='user_id'
    )
    
    class Meta:
        model = Message
        fields = ['url', 'message_id', 'sender', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
        extra_kwargs = {
            'url': {'view_name': 'message-detail', 'lookup_field': 'message_id'},
            'sender': {'view_name': 'user-detail', 'lookup_field': 'user_id'}
        }

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    participants = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all(),
        many=True,
        lookup_field='user_id'
    )
    
    class Meta:
        model = Conversation
        fields = ['url', 'conversation_id', 'participants', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
        extra_kwargs = {
            'url': {'view_name': 'conversation-detail', 'lookup_field': 'conversation_id'},
            'participants': {'view_name': 'user-detail', 'lookup_field': 'user_id'}
        }


    participants = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True,
        many=True,
        lookup_field='user_id'
    )
    participant_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['url', 'conversation_id', 'participants', 'participant_count', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
        extra_kwargs = {
            'url': {'view_name': 'conversation-detail', 'lookup_field': 'conversation_id'},
            'participants': {'view_name': 'user-detail', 'lookup_field': 'user_id'}
        }
    
    def get_participant_count(self, obj):
        return obj.participants.count()