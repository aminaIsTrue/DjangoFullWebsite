from django.urls import path
from . import views

urlpatterns = [
    path('',views.projects, name="projects-path"),
    path('project/<str:pk>',views.project, name="project-path"),
    path('create-project/',views.createProject, name="createProject-path"),
    path('update-project/<str:pk>',views.updateProject, name="updateProject-path"),
    path('delete-project/<str:pk>',views.deleteProject, name="deleteProject-path"),
]