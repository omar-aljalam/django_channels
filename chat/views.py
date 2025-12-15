from django.shortcuts import render, redirect

from django.views.generic import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from .models import Message, UserChannel

class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "chat/index.html")
    
class LoginView(View):
    def get(self, request):
        return render(request, "chat/login.html")
    
    def post(self, request):
        data = request.POST
        username = data.get("username")
        password = data.get("password")
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return redirect("home")
        else:
            message = {"error": "Invalid username or password"}
            return render(request, "chat/login.html", message)

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")
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
        logout(request)
        return redirect("main")


class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        user = User.objects.get(id=request.user.id)
        users = User.objects.filter(is_superuser=False).exclude(id=request.user.id)
        return render(request, "chat/home.html", {
            "user": user,
            "users": users
        })

class ChatPersonView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return redirect("login")
        me = User.objects.get(id=request.user.id)
        person = User.objects.get(id=pk)
        messages = Message.objects.filter(Q(sender=me, receiver=person) | Q(sender=person, receiver=me)).order_by("date")
        data = {
                "type": "chat_message",
                "type_of_data": "read_message"
            }
        channel_layer = get_channel_layer()
        receiver_channel = UserChannel.objects.get(user=person)
        async_to_sync(channel_layer.send)(receiver_channel.channel_name, data)

        Message.objects.filter(
                receiver=person,
                sender=me,
            ).update(is_read=True)
        return render(request, "chat/chat_person.html", {
            "me": me,
            "person": person,
            "messages": messages
        })