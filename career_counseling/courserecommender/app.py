import os
from flask import Flask, render_template, request
import google.generativeai as genai
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

# Debug: Check if API key is loading
print(f"API Key: {API_KEY}")

# Configure Google Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        skills = request.form.get("skills")
        interests = request.form.get("interests")
        department = request.form.get("department")

        # Generate recommendations using Gemini API
        recommendations = get_course_recommendations(skills, interests, department)
        return render_template("results.html", recommendations=recommendations)
    
    return render_template("index.html")

def get_course_recommendations(skills, interests, department):
    prompt = f"""
    Suggest 5 to 7 online courses for a student in {department} with skills in {skills} and interests in {interests}.
    Format the result in this EXACT format:

    1. Course Name (Platform: https://example.com)  
    2. Course Name (Platform: https://example.com)  
    3. Course Name (Platform: https://example.com)  

    Make sure to include valid, real course links from Coursera, Udemy, edX, and Swayam.
    Do not provide search suggestions — provide direct links only.
    """

    try:
        response = model.generate_content(prompt)
        print("RAW RESPONSE:", response.text)

        courses = []
        # ✅ Updated regex to capture all platforms correctly
        pattern = r"(.+?) \((Coursera|Udemy|edX|Swayam): (https?://[^\)]+)\)"
        matches = re.findall(pattern, response.text)

        for match in matches:
            course = {"name": match[0], "platform": match[1], "link": match[2]}
            courses.append(course)

        # ✅ Format the output properly
        formatted_courses = []
        for course in courses[:7]:
            formatted_courses.append({
                "name": f"{course['name']} ({course['platform']})",
                "link": course["link"]
            })

        return formatted_courses
    except Exception as e:
        print(f"Error: {e}")
        return [{"name": "Failed to fetch courses", "link": "#"}]

def extract_course_names(text):
    pattern = r"^\d+\.\s+(.+)$"
    matches = re.findall(pattern, text, re.MULTILINE)
    return matches

# Fallback 2: Generate Search Links (Now with platform names)
def generate_fallback_links(course_names):
    platforms = {
        "Coursera": "https://www.coursera.org/search?query=",
        "Udemy": "https://www.udemy.com/courses/search/?q=",
        "edX": "https://www.edx.org/search?q=",
        "Swayam": "https://swayam.gov.in/search?query="
    }

    courses = []
    for course in course_names:
        for platform, url in platforms.items():
            search_link = f"{url}{course.replace(' ', '+')}"
            courses.append({"name": f"{course} ({platform})", "link": search_link})
            break

    return courses

# New Function: Identify Platform Name from URL
def get_platform_name(link):
    if "coursera.org" in link:
        return "Coursera"
    elif "udemy.com" in link:
        return "Udemy"
    elif "edx.org" in link:
        return "edX"
    elif "swayam.gov.in" in link:
        return "Swayam"
    else:
        return "Other"



if __name__ == "__main__":
    app.run(debug=True)
