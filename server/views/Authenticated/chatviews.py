from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from server.models import chatModels
from server.models.chatModels import ChatSession, ChatFile

import sounddevice as sd
from transformers import SeamlessM4Tv2Model, AutoProcessor

tts_model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")

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


def processMessagesAndFilesNew(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    response_data = {}
    message = request.POST.get('message', None)
    try:
        print(message)
        if message:
            aiResponse = "AI response to \"" + message + "\""
            print(aiResponse)
            
            inputs = processor(text = aiResponse, src_lang="eng", return_tensors="pt")
            audio_array = tts_model.generate(**inputs, tgt_lang="eng")[0].cpu().numpy().squeeze()
            sd.play(audio_array, tts_model.config.sampling_rate)

            response_data['api_response'] = aiResponse
            return JsonResponse(response_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

