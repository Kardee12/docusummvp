from django.shortcuts import render


def index(request):
    context = {}
    return render(request, "docusum/noauth/index.html", context)


def logView(request):
    return render(request, 'sumApp/login.html')
