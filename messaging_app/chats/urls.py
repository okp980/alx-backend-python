from django.urls import path, include
from rest_framework import routers
from drf_nested_routers import NestedDefaultRouter

from .views import ConversationViewSet, MessageViewSet 

# Create a router and register our ViewSets with it.
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Create a nested router for messages within conversations
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
