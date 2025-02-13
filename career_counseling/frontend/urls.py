from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.signup_view, name='home'),  # Homepage (Signup Page)
    path('signup/', views.signup_view, name='signup'),  # Signup Page
    path('login/', views.login_view, name='login'),  # Login Page
    path('login.html', lambda request: render(request, 'login.html')),  # Direct login.html access (Optional)
    path('home/', views.index, name='index'),  # 🔹 Main page after login
    path('index.html', lambda request: render(request, 'index.html')),  # Optional direct access
    path('logout/', views.logout_view, name='logout'),  # 🔹 Logout Route
    path('profile/', views.profile_view, name='profile'),
]
