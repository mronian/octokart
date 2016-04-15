from django.contrib import admin
from transactions.models import Message, Connection
# Register your models here.

admin.site.register(Message)
admin.site.register(Connection)