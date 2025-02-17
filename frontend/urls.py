from django.urls import path
from django.shortcuts import render
from . import views
from .views import file_view, skill_management_view,save_profile,save_skill  # Import both views

urlpatterns = [
    path('', views.signup_view, name='home'),  # Homepage (Signup Page)
    path('signup/', views.signup_view, name='signup'),  # Signup Page
    path('login/', views.login_view, name='login'),  # Login Page
    path('login.html', lambda request: render(request, 'login.html')),  # Direct login.html access (Optional)
    path('home/', views.index, name='index'),  # 🔹 Main page after login
    path('index.html', lambda request: render(request, 'index.html')),  # Optional direct access
    path('logout/', views.logout_view, name='logout'),  # 🔹 Logout Route
    path('profile/', views.profile_view, name='profile'),  # Profile Page

    # ✅ Corrected Routes
   
    path("save-profile/", save_profile, name="save_profile"),
    path('file/', file_view, name='file'),  # Route for File Page
    path('skillmanagement/', skill_management_view, name='skillmanagement'),  # Route for Skill Management Page
    path("save-skill/", save_skill, name="save_skill"),
     
]
