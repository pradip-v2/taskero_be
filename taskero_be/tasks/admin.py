from django.contrib import admin

from taskero_be.tasks.models import Task

admin.site.register(Task)
