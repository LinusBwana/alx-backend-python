from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'messages',views.MessageViewSet, basename="messages")
router.register(r'conversations', views.ConversationViewSet, basename="conversations")

urlpatterns = [
    path('', include(router.urls)),
]