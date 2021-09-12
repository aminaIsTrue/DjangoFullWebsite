from collections import namedtuple
from django.shortcuts import render,redirect
from.models import Profile, Skill
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from django.db.models import Q
from .utils import searchProfiles,paginateProfile
# Create your views here.

def profiles(request):
    profiles, search_query = searchProfiles(request)
    customRange, profiles = paginateProfile(request,profiles,2)
    context = {'profiles':profiles, 'search_query':search_query,'customRange':customRange}
    return render(request,'users/profiles.html',context)

def UserProfile(request,pk):
   profileUser = Profile.objects.get(id = pk)
   context = {'profileUser':profileUser}
   return render(request,'users/user-profile.html',context)


def loginUser(request):
    page = 'login'
    context ={'page':page}
    #here, we do not want the athenticated user to see the login page because she/he already authenticated
    #no need to land in that page again!
    if request.user.is_authenticated:
        return redirect('profiles-path')
    if request.method ==  'POST':
        username = request.POST['username']
        password = request.POST['password']  

        try:
            user = User.objects.get(username = username) 
        except:
            messages.error(request, 'The username does not exist, please try again!') 
        
        user = authenticate(request, username= username, password= password)

        if user is not None:
            #the login method will:
            # 1- creat a seesion for this user in the database
            #2- add the session information to the browser's cookies
            login(request,user)
            return redirect('profiles-path')
        else:
            #even if we checked the username but we still ne to  say the either username or password are incorrect
            #because it may that the person has entered a correct username that it is not her/his
            #better not to give the hint that such a username exists!
            messages.error(request, 'Username Or The password is not correct, try again!')

    return render(request,'users/login-register.html',context)


def logoutUser(request):

    # for the logout we just pass-in  request 
    # by that we delete the **session** of that user which means an authentication is needed
    logout(request)
    messages.info(request, 'User loged out!') 
    return redirect('login-path')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    context ={'page':page, 'form':form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            #we want the username to be saved lowercased in the database
            #thats why we:
            #  1- hold the user, (another reason to hold the user is to log him/her in automatically using login(request,user))
            # 2-set the commit to false until making sure the username is lowercased, 
            # 3- then save the user in the database  
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account is created!')
            login(request,user)
            return redirect('edit-account-path')
        else:
            messages.error(request, 'An error has occured during registration!')
    return render(request,'users/login-register.html',context)
@login_required(login_url='login-path')
def userAccount(request):
    #we can get the user from the request (it is one of the info in the dictionary)
    #each user created we has the profile automatically created
    profileUser = request.user.profile
    projects = profileUser.project_set.all()
    context = {'profileUser': profileUser,'projects': projects}
    return render(request,'users/account.html',context)

@login_required(login_url='edit-account-path')
def editAccount(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance = profile)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid:
            # because it is an update we need to mention the instance
            #and since we are sending images as well we neet to mention request.FILES
         profile = ProfileForm(request.POST,request.FILES,instance = profile )
         profile.save()
         return redirect('account-path')
        
    return render(request,'users/profile-form.html',context)


login_required(login_url='login-path')
def createSkill(request):
    form = SkillForm()
    context = {'form':form}
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid:
            profile = request.user.profile
            skill = form.save(commit = False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill added successfully!')
            return redirect('account-path')

    return render(request,'users/skill_form.html',context)

login_required(login_url='login-path')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    # to have the form populated with the info we want to update
    form = SkillForm(instance=skill)
    context = {'form':form}
    if request.method == 'POST':
        #we give the request.POST data and the instance we want to update ==>change the instance with the request.POST info!
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid:
            form.save()
            messages.success(request, 'Skill updated successfully!')
            return redirect('account-path')

    return render(request,'users/skill_form.html',context)


@login_required(login_url='login-path')
def deleteSkill(request,pk):
    skill = request.user.profile.skill_set.get(id= pk)
    if request.method == 'POST':
            skill.delete()
            messages.success(request, 'Skill deleted successfully!')
            return redirect ("account-path")

    context = {'object':skill}
    return render(request,'delete_template.html',context)