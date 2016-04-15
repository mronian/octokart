from django.contrib import admin
from locks.models import SellerQueue, ItemLock, SellerLock, ItemQueue
# Register your models here.

admin.site.register(SellerQueue)
admin.site.register(ItemLock)
admin.site.register(SellerLock)
admin.site.register(ItemQueue)
