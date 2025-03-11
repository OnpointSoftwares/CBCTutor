import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import json
# Configure Gemini API
genai.configure(api_key="AIzaSyBXVv3tklwuNRpH82WbP-bLyNAVQA-kvYo")
model =genai.GenerativeModel("gemini-1.5-flash")

# CBC Curriculum Data
cbc_data = {
    "grade": 3,
    "curriculum": {
        "Literacy": "Developing reading and writing skills in both English and Kiswahili to enhance communication.",
        "Kiswahili Language Activities": "Building foundational skills in Kiswahili to improve oral and written communication.",
        "English Language Activities": "Strengthening English language proficiency through listening, speaking, reading, and writing activities.",
        "Indigenous Language Activities": "Promoting the use of mother tongue to preserve cultural identity and enhance early learning.",
        "Mathematical Activities": "Introducing basic arithmetic, problem-solving, and number operations for logical thinking.",
        "Environmental Activities": "Teaching about nature, the environment, and conservation to promote sustainability.",
        "Hygiene and Nutrition": "Educating on personal hygiene, healthy eating habits, and overall well-being.",
        "Religious Education": "Providing moral and spiritual development through Christian, Islamic, or Hindu religious studies.",
        "Movement and Creative Activities": "Encouraging artistic expression, music, dance, drama, and physical fitness."
    },
    "resources": {
        "KICD": "https://kicd.ac.ke/cbc-materials/curriculum-designs/",
        "EasyElimu": "https://www.easyelimu.com/2018/itemlist/category/193-grade-3",
        "CBC Syllabus App": "https://play.google.com/store/apps/details?id=cbc.resources.teachersarena.grade3syllabus"
    }
}

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

def ask_gemini(question):
    """Generates response using Gemini AI with CBC context."""
    cbc_content = fetch_cbc_content()
    cbc_json = json.dumps(cbc_data, indent=2)

    prompt = f"""
    You are an AI expert in the Kenyan CBC curriculum. Use the following CBC curriculum data to answer the question.

    CBC Curriculum Data:
    {cbc_json}

    Additional Web-Scraped Content:
    {cbc_content}

    Question: {question}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error with Gemini AI: {e}"

# Example usage
user_question = "What subjects are covered in Grade 3 CBC?"
response = ask_gemini(user_question)
print(response)