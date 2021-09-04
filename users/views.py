from django.shortcuts import render,redirect
from.models import Profile, Skill
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
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
    messages.error(request, 'User loged out!') 
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
            return redirect('profiles-path')
        else:
            messages.error(request, 'An error has occured during registration!')
    return render(request,'users/login-register.html',context)