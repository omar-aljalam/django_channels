from django.shortcuts import render, redirect

from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

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

    def post(self, request):
        message = {}
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if User.objects.filter(username=username).exists():
            message = {"error": "Username already exists"}
            return render(request, "chat/register.html", message)
        
        if User.objects.filter(email=email).exists():
            message = {"error": "Email already exists"}
            return render(request, "chat/register.html", message)
        
        user = User.objects.create_user(username=username, email=email,  first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        user = authenticate(request=request, username=username,password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect("home")
        else:
            message = {"error": "Registration failed. Please try again."}
            return render(request, "chat/register.html", message)

class LogoutView(View):
    def get(self, request):
        pass

class HomeView(View):
    def get(self, request):
        return render(request, "chat/home.html")

class ChatPersonView(View):
    def get(self, request):
        return render(request, "chat/chat_person.html")