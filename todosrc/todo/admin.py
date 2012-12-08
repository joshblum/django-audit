from dbe.todo.models import *
from django.contrib import admin

admin.site.register(Item, ItemAdmin)
admin.site.register(DateTime, DateAdmin)
