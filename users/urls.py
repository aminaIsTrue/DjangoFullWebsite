from django.urls import path
from . import views

urlpatterns = [
    path('',views.profiles,name='profiles-path'),
    path('profile/<str:pk>/',views.UserProfile,name='userProfile-path')
]
