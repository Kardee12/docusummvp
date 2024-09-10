from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    model_used = models.CharField(max_length=255, help_text="The AI model used in the chat.")
    prompt = models.TextField(null=True, blank=True, help_text="Initial prompt for the chat session, if any.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ChatMessage(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=255)  # User or AI
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}"


class ChatFile(models.Model):
    chatSession = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='chat_files/', help_text="Uploaded file for the chat session.")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.chat_session.name}: {self.file.name}"
