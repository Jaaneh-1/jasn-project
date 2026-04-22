from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ['role', 'contenu', 'date']


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display  = ['id', 'utilisateur', 'date_creation']
    list_filter   = ['date_creation']
    inlines       = [MessageInline]