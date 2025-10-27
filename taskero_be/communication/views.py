from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework_extensions.mixins import NestedViewSetMixin

from taskero_be.communication.models import Conversation
from taskero_be.communication.models import Message
from taskero_be.communication.serializers import ConversationSerializer
from taskero_be.communication.serializers import MessageSerializer
from taskero_be.pagination import BeforeIdPagination


class ConversationViewSet(viewsets.ModelViewSet[Conversation]):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        "participants": ["exact"],
        "type": ["exact"],
    }
    search_fields = ["participants__name", "name"]


class MessageViewSet(viewsets.ModelViewSet[Message]):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_fields = {
        "conversation": ["exact"],
        "sender": ["exact"],
        "conversation__participants": ["exact"],
    }
    search_fields = ["content"]


class ConversationMessagesViewSet(
    NestedViewSetMixin,
    ListModelMixin,
    viewsets.GenericViewSet[Message],
):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    model = Message
    pagination_class = BeforeIdPagination
