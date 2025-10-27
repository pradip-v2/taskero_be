from django.contrib import admin

from taskero_be.communication.models import Conversation
from taskero_be.communication.models import Message
from taskero_be.communication.models import MessageAttachment

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(MessageAttachment)
