from django.urls import path
from .views import *

urlpatterns = [
    path("chatbot/", chatbot_view, name="cbc-chatbot"),
    path("", HomeView, name="home"),
]
