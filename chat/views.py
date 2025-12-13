from django.shortcuts import render

from django.views.generic import View

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

class IndexView(View):
    def get(self, request):
        data = {
            "type": "receiver",
            "text_data":{
                "title": "Chat Application",
                "header": "Welcome to the Chat App"
                }
            }
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("group_chat", data)
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