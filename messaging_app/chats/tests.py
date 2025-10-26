import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from rest_framework import status
from .models import User, Conversation, Message

User = get_user_model()


class UserModelTests(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
            role='guest'
        )
    
    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'guest')
        self.assertIsNotNone(self.user.user_id)
    
    def test_user_str_method(self):
        """Test user string representation"""
        expected_str = f"{self.user.username} ({self.user.email})"
        self.assertEqual(str(self.user), expected_str)


class ConversationModelTests(TestCase):
    """Test cases for Conversation model"""
    
    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123',
            first_name='User',
            last_name='One',
            role='guest'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123',
            first_name='User',
            last_name='Two',
            role='host'
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)
    
    def test_conversation_creation(self):
        """Test conversation creation"""
        self.assertIsNotNone(self.conversation.conversation_id)
        self.assertEqual(self.conversation.participants.count(), 2)
    
    def test_conversation_participants(self):
        """Test conversation participants"""
        self.assertIn(self.user1, self.conversation.participants.all())
        self.assertIn(self.user2, self.conversation.participants.all())


class MessageModelTests(TestCase):
    """Test cases for Message model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='sender',
            email='sender@example.com',
            password='testpass123',
            first_name='Sender',
            last_name='User',
            role='guest'
        )
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user)
        self.message = Message.objects.create(
            sender=self.user,
            conversation=self.conversation,
            message_body='Test message'
        )
    
    def test_message_creation(self):
        """Test message creation"""
        self.assertIsNotNone(self.message.message_id)
        self.assertEqual(self.message.sender, self.user)
        self.assertEqual(self.message.conversation, self.conversation)
        self.assertEqual(self.message.message_body, 'Test message')
    
    def test_message_str_method(self):
        """Test message string representation"""
        expected_str = f"Message from {self.user.username} in {self.conversation.conversation_id}"
        self.assertEqual(str(self.message), expected_str)


@pytest.mark.django_db
class APITests:
    """Test cases for API endpoints"""
    
    def test_conversation_api_endpoint(self):
        """Test that conversation endpoint exists"""
        client = Client()
        # This will test if the endpoint is accessible
        # Note: Actual implementation would require authentication
        pass


# Simple sanity check
def test_project_structure():
    """Test that project structure is correct"""
    assert User is not None
    assert Conversation is not None
    assert Message is not None
