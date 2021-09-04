from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser,name='login-path'),
    path('logout/',views.logoutUser,name='logout-path'),
    path('register/',views.registerUser,name='register-path'),
    path('',views.profiles,name='profiles-path'),
    path('profile/<str:pk>/',views.UserProfile,name='userProfile-path')
]
