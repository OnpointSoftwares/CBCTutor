import google.generativeai as genai
import requests
from django.shortcuts import render
from bs4 import BeautifulSoup
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .gemini import ask_gemini
# Configure Gemini API
genai.configure(api_key="AIzaSyBXVv3tklwuNRpH82WbP-bLyNAVQA-kvYo")
model =genai.GenerativeModel("gemini-1.5-flash")

def fetch_cbc_content():
    """Scrapes CBC curriculum content from the KICD website."""
    url = "https://kicd.ac.ke/curriculum-reform/basic-education-curriculum-framework/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup.get_text()
    except Exception as e:
        return f"Error fetching CBC content: {e}"

    return "CBC curriculum information is unavailable."
def HomeView(request):
    return render(request, "index.html")
@csrf_exempt  # Exempt from CSRF verification
@api_view(['POST'])
def chatbot_view(request):
    """Handles user questions about CBC and returns Gemini AI responses."""
    question = request.data.get("question")

    if not question:
        return Response({"error": "Question is required"}, status=status.HTTP_400_BAD_REQUEST)

    response = ask_gemini(question)
    return Response({"response": response}, status=status.HTTP_200_OK)