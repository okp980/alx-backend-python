from django.urls import path, include
from rest_framework_nested import routers

from .views import ConversationViewSet, MessageViewSet 

# Create a router and register our ViewSets with it.
router = routers.SimpleRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Create a nested router for messages within conversations
nested_router = routers.NestedSimpleRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]
