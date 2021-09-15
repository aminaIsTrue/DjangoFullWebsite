from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginUser,name='login-path'),
    path('logout/',views.logoutUser,name='logout-path'),
    path('register/',views.registerUser,name='register-path'),
    path('',views.profiles,name='profiles-path'),
    path('profile/<str:pk>/',views.UserProfile,name='userProfile-path'),
    path('account/',views.userAccount,name='account-path'),
    path('edit-account/',views.editAccount,name='edit-account-path'),
    path('create-skill/',views.createSkill,name='create-skill-path'),
    path('update-skill/<str:pk>/',views.updateSkill,name='update-skill-path'),
    path('delete-skill/<str:pk>/',views.deleteSkill,name='delete-skill-path'),
    path('inbox/',views.inbox,name='inbox-path'),
    path('message/<str:pk>/',views.viewMessage,name='viewMessage-path'),
    path('create-message/<str:pk>/',views.createMessge,name='create-message-path'),
]
