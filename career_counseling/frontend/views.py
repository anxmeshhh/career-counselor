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