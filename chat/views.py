from django.shortcuts import render

from django.views.generic import View

class IndexView(View):
    def get(self, request):
        return render(request, "chat/index.html")
    
class LoginView(View):
    def get(self, request):
        return render(request, "chat/login.html")

class RegisterView(View):
    def get(self, request):
        return render(request, "chat/register.html")

class LogoutView(View):
    def get(self, request):
        pass

class HomeView(View):
    def get(self, request):
        return render(request, "chat/home.html")

class ChatPersonView(View):
    def get(self, request):
        return render(request, "chat/chat_person.html")