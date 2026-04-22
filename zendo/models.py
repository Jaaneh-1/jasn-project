from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """
    Une session de conversation avec Zendo.
    Chaque utilisateur peut avoir plusieurs conversations.
    """
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='conversations',
        verbose_name='Utilisateur'
    )
    # Pour les visiteurs non connectés on utilise la session
    session_key = models.CharField(max_length=40, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
        ordering = ['-date_creation']

    def __str__(self):
        who = self.utilisateur.username if self.utilisateur else f'Visiteur ({self.session_key[:8]})'
        return f'Conversation de {who} — {self.date_creation.strftime("%d/%m/%Y %H:%M")}'


class Message(models.Model):
    """Un message dans une conversation Zendo"""

    class Role(models.TextChoices):
        USER      = 'user',      'Utilisateur'
        ASSISTANT = 'assistant', 'Zendo'

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role    = models.CharField(max_length=10, choices=Role.choices)
    contenu = models.TextField()
    date    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['date']

    def __str__(self):
        return f'[{self.get_role_display()}] {self.contenu[:60]}...'