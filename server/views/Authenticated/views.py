from allauth.account.views import LoginView
from django.shortcuts import render, redirect


# Create your views here.
class CustomLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        return redirect('/dashboard')


def workspace(request):
    return render(request, "docusum/authenticated/workspace.html")
