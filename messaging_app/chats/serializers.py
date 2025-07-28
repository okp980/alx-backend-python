from rest_framework import serializers
from .models import User, Message, Conversation

class UserSerializer(serializers.Serializer):
    user_id = serializers.UUIDField(read_only=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    first_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=150, required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    created_at = serializers.DateTimeField(read_only=True)
    password_hash = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing User instance, given the validated data.
        """
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.role = validated_data.get('role', instance.role)
        if 'password_hash' in validated_data:
            instance.password_hash = validated_data.get('password_hash')
        instance.save()
        return instance

    def validate_email(self, value):
        """
        Check that the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

class MessageSerializer(serializers.Serializer):
    message_id = serializers.UUIDField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    message_body = serializers.CharField()
    sent_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new Message instance, given the validated data.
        """
        return Message.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Message instance, given the validated data.
        """
        instance.sender = validated_data.get('sender', instance.sender)
        instance.message_body = validated_data.get('message_body', instance.message_body)
        instance.save()
        return instance

class ConversationSerializer(serializers.Serializer):
    conversation_id = serializers.UUIDField(read_only=True)
    participants = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True
    )
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        Create and return a new Conversation instance, given the validated data.
        """
        participants = validated_data.pop('participants')
        conversation = Conversation.objects.create(**validated_data)
        conversation.participants.set(participants)
        return conversation

    def update(self, instance, validated_data):
        """
        Update and return an existing Conversation instance, given the validated data.
        """
        if 'participants' in validated_data:
            participants = validated_data.pop('participants')
            instance.participants.set(participants)
        instance.save()
        return instance

