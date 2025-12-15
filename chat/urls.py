from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="main"),
    path('login', views.LoginView.as_view(), name="login"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('logout', views.LogoutView.as_view(), name="logout"),
    path('home', views.HomeView.as_view(), name="home"),
    path('chat_person/<int:pk>', views.ChatPersonView.as_view(), name="chat_person"),
]
