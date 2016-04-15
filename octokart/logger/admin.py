from django.contrib import admin

# Register your models here.
from .models import TransactionLog, CommitLog, LockLog, LoginLog

admin.site.register(TransactionLog)
admin.site.register(CommitLog)
admin.site.register(LockLog)
admin.site.register(LoginLog)
