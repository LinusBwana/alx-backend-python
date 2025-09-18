from django.urls import include, path
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename="conversations")

conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', views.MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]

# router = routers.DefaultRouter()
# router.register(r'messages',views.MessageViewSet, basename="messages")
# router.register(r'conversations', views.ConversationViewSet, basename="conversations")

# urlpatterns = [
#     path('', include(router.urls)),
# ]