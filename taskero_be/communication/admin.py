from django.contrib import admin

from taskero_be.communication.models import Conversation
from taskero_be.communication.models import Message

admin.site.register(Conversation)
admin.site.register(Message)
