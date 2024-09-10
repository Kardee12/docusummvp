from django.shortcuts import render
from django.views import View

from server.models.chatModels import ChatSession


# Create your views here.

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        chat_sessions = ChatSession.objects.filter(owner=request.user)
        print(chat_sessions)
        context = {}
        context.update({'chat_sessions': chat_sessions})
        return render(request, "docusum/authenticated/dashboard.html", context)
