from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from server.models import chatModels
from server.models.chatModels import ChatSession, ChatFile


def createChatSession(request):
    if request.method == 'POST':
        name = request.POST.get('chatName')
        model = request.POST.get('chatModel')
        prompt = request.POST.get('chatPrompt', None)
        chatSession = chatModels.ChatSession(
            name=name,
            owner=request.user,
            model_used=model,
            prompt=prompt
        )
        if ChatSession.objects.filter(name=name).exists():
            return JsonResponse({"error": "ChatSession already exists"}, status=400)

        chatSession.save()
        if 'chatFile' in request.FILES:
            files = request.FILES.getlist('chatFile', None)
            for file in files:
                cfile = chatModels.ChatFile(
                    chatSession=chatSession,
                    file=file
                )
                cfile.save()
        print(chatSession.__str__())
        print(f"Chat session created: {chatSession}")
        return JsonResponse({'chat_id': chatSession.id})
    return JsonResponse({'error': 'Invalid method'}, status=400)


def viewChatSession(request, chat_id):
    chat_session = get_object_or_404(ChatSession, id=chat_id, owner=request.user)
    messages = chat_session.messages.all().values('sender', 'message', 'timestamp')
    files = chat_session.files.all().values('file', 'uploaded_at')
    return JsonResponse({
        'name': chat_session.name,
        'model_used': chat_session.model_used,
        'prompt': chat_session.prompt,
        'messages': list(messages),
        'files': list(files),
    })


def uploadFilesToChat(request, chat_id):
    if request.method == 'POST' and request.FILES.get('file'):
        chat_session = get_object_or_404(ChatSession, id=chat_id, owner=request.user)
        file = request.FILES['file']

        chat_file = ChatFile.objects.create(chat_session=chat_session, file=file)

        return JsonResponse({'file_id': chat_file.id, 'file_name': chat_file.file.name})
    return JsonResponse({'error': 'Invalid method or missing file'}, status=400)


def renameChat(request, chat_id):
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        chat = get_object_or_404(ChatSession, id=chat_id, owner=request.user)
        chat.name = new_name
        chat.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def deleteChat(request, chat_id):
    if request.method == 'DELETE':
        chat = get_object_or_404(ChatSession, id=chat_id, owner=request.user)
        chat.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def testChat(request):
    return render(request, 'docusum/authenticated/chats/chat.html')
