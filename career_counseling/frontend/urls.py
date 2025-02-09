from django.urls import path
from . import views

urlpatterns = [
  #  path('', views.signup_view, name='signup'),  # First page (Signup)
  #  path('login/', views.login_view, name='login'),  # Login page
    path('', views.index, name='index'),  # Main page after login
]
