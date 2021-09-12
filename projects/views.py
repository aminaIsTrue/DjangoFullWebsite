from django.core import paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from .forms import ProjectForm
from django.contrib import messages
from django.db.models import Q
from .utils import searchProjects,paginateProject

# Create your views here.
def projects(request):
    projects, search_query = searchProjects (request)
    customRange, projects = paginateProject(request,projects,6)

    context = {'projects': projects , 'search_query': search_query, 'customRange':customRange}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projetObj = Project.objects.get(id = pk)
    tags = projetObj.tags.all()
    context = {"projetObj":projetObj, 'tags':tags}
    return render(request,'projects/single-project.html',context)
    
@login_required(login_url = 'login-path')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit = False)
            project.owner = profile
            project.save()
            messages.success(request, 'Project Created successfully!')
            return redirect("account-path")
    context = {'form':form}
    return render(request,'projects/project_form.html',context)


@login_required(login_url = 'login-path')
def updateProject(request,pk):
    project = Project.objects.get(id= pk)
    ProjectOwner = project.owner
    profile =  request.user.profile
    # we need to make sure that even if another user has the link to edit a project he can not do it
    if ProjectOwner == profile:
        form = ProjectForm(instance=project)
        if request.method == 'POST':
            form = ProjectForm(request.POST,  request.FILES,instance=project)
            if form.is_valid():
                form.save()
                messages.success(request, 'Project Updated successfully!')
                return redirect("account-path")
    else:
        return redirect("login-path")
    context = {'form':form}
    return render(request,'projects/project_form.html',context)
@login_required(login_url='login-path')
def deleteProject(request,pk):
    project = Project.objects.get(id= pk)
    ProjectOwner = project.owner
    profile =  request.user.profile
    # we need to make sure that even if another user has the link to delete a project he can not do it
    if ProjectOwner == profile:
        if request.method == 'POST':
            project.delete()
            messages.success(request, 'Project deleted successfully!')
            return redirect ("account-path")
    else:
        return redirect("login-path")
    context = {'object':project}
    return render(request,'delete_template.html',context)