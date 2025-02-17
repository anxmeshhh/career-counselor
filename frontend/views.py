from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import mysql.connector

# 🔹 Function to establish MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="theanimesh2005",  # Change to your actual MySQL password
        database="careerhub_db"
    )

# 🔹 Signup View
def signup_view(request):
    messages.get_messages(request).used = True  # Clears old messages

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        aadhaar_no = request.POST.get("aadhaar_no", "").strip()

        if not all([full_name, email, password, aadhaar_no]):
            messages.error(request, "All fields are required!")
            return redirect("signup")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Check if the email is already registered
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                messages.error(request, "Email already registered! Please login.")
                return redirect("login")

            # Insert the user into the database (without hashing the password)
            cursor.execute(
                "INSERT INTO users (full_name, email, password, aadhaar_no) VALUES (%s, %s, %s, %s)",
                (full_name, email, password, aadhaar_no)
            )
            conn.commit()

            cursor.close()
            conn.close()

            messages.success(request, "Signup successful! Please log in.")
            return redirect("login")  # ✅ Redirects to login page

        except mysql.connector.Error as e:
            messages.error(request, f"Database error: {str(e)}")
            return redirect("signup")

    return render(request, "signup.html")

# 🔹 Login View
def login_view(request):
    messages.get_messages(request).used = True  # Clears old messages

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if not email or not password:
            messages.error(request, "All fields are required!")
            return redirect("login")

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Check if the user exists
            cursor.execute("SELECT full_name, password FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            cursor.close()
            conn.close()

            if user and password == user["password"]:  # Plain-text password check
                request.session["user_email"] = email
                request.session["user_name"] = user["full_name"]

                messages.success(request, f"Welcome, {user['full_name']}! You are now logged in.")
                return redirect("index")  
            else:
                messages.error(request, "Invalid email or password!")
                return redirect("login")

        except mysql.connector.Error as e:
            messages.error(request, f"Database error: {str(e)}")
            return redirect("login")

    return render(request, "login.html")

# 🔹 Logout View
def logout_view(request):
    request.session.flush()  
    messages.success(request, "You have been logged out.")
    return redirect("login")

# 🔹 Dashboard/Home Page
def index(request):
    if "user_email" not in request.session:
        messages.error(request, "Please log in first.")
        return redirect("login")

    return render(request, "index.html", {"user_name": request.session.get("user_name")})



def profile_view(request):
    return render(request, 'profile.html')

def file_view(request):
    return render(request, "file.html")  # Render the file.html template


from django.shortcuts import render

def skill_management_view(request):
    return render(request, "skillmanagement.html")  # Renders the skill management page


from django.http import JsonResponse


def save_profile(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    connection = get_db_connection()
    if not connection:
        return JsonResponse({"error": "Database connection failed"}, status=500)

    cursor = connection.cursor()

    try:
        # Get form data
        email = request.POST.get("email", "").strip()
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        age = request.POST.get("age", "").strip()
        experience = request.POST.get("experience", "").strip()
        city = request.POST.get("city", "").strip()
        state = request.POST.get("state", "").strip()
        country = request.POST.get("country", "").strip()
        skills = request.POST.get("skills", "").strip()
        education = request.POST.get("education", "").strip()
        interests = request.POST.get("interests", "").strip()

        # Check if email exists
        cursor.execute("SELECT 1 FROM user_profiles WHERE email = %s", (email,))
        profile_exists = cursor.fetchone()

        if profile_exists:
            # Update profile
            sql = """
                UPDATE user_profiles 
                SET name=%s, phone=%s, age=%s, experience=%s, city=%s, state=%s, 
                    country=%s, skills=%s, education=%s, interests=%s
                WHERE email=%s
            """
            values = (name, phone, age, experience, city, state, country, skills, education, interests, email)
        else:
            # Insert new profile
            sql = """
                INSERT INTO user_profiles (email, name, phone, age, experience, city, state, country, skills, education, interests)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (email, name, phone, age, experience, city, state, country, skills, education, interests)

        cursor.execute(sql, values)
        connection.commit()

        return JsonResponse({"message": "Profile saved successfully!"}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Database error: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()



from django.http import JsonResponse
import mysql.connector


def save_skill(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=405)

    print("Received Data:", request.POST)  # Debugging: Check what data is received

    connection = get_db_connection()
    if not connection:
        return JsonResponse({"error": "Database connection failed"}, status=500)

    cursor = connection.cursor()

    try:
        # Get form data (trim to avoid spaces)
        skill_name = request.POST.get("skill_name", "").strip()
        skill_id = request.POST.get("skill_id", "").strip()
        skill_category = request.POST.get("skill_category", "").strip()
        skill_type = request.POST.get("skill_type", "").strip()
        skill_level = request.POST.get("skill_level", "").strip()
        learning_status = request.POST.get("learning_status", "").strip()
        certifications = request.POST.get("certifications", "").strip()
        learning_notes = request.POST.get("learning_notes", "").strip()

        print("Parsed Data:", skill_name, skill_id, skill_category, skill_type, skill_level, learning_status, certifications, learning_notes)

        # Ensure required fields are not empty
        if not skill_name or not skill_id or not skill_category or not skill_type or not skill_level or not learning_status:
            return JsonResponse({"error": "Please fill all required fields."}, status=400)

        # Insert into database
        sql = """
            INSERT INTO skills (skill_name, skill_id, skill_category, skill_type, 
                                skill_level, learning_status, certifications, learning_notes) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (skill_name, skill_id, skill_category, skill_type, skill_level, learning_status, certifications, learning_notes)

        cursor.execute(sql, values)
        connection.commit()

        return JsonResponse({"message": "Skill saved successfully!"}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Database error: {str(e)}"}, status=500)

    finally:
        cursor.close()
        connection.close()

