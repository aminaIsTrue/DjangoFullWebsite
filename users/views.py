from django.shortcuts import render
from.models import Profile, Skill
# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles':profiles}
    return render(request,'users/profiles.html',context)

def UserProfile(request,pk):
   profileUser = Profile.objects.get(id = pk)
   context = {'profileUser':profileUser}
   return render(request,'users/user-profile.html',context)