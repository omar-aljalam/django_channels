from django.contrib import admin
from .models import Message, UserChannel

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "date", "is_read")
    readonly_fields = ("sender", "receiver", "date", "message", "is_read")

admin.site.register(Message, MessageAdmin)
admin.site.register(UserChannel)
