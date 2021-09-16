from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Profile
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save,sender = User)
def createProfile(sender,instance,created,**kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,
        )
        subject = 'Welcome to our Website'
        message = 'We are glad you are here!'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

# we have already created a form for updating ptofile but we want 
#at the same time update the user that's why we will use a post_save signal
@receiver(post_save,sender = Profile)
def updateUser(sender,instance,created,**kwargs):
    profile = instance
    user = profile.user
    # the created check here is for not falling into a recursion area 
    # if not checked than it will be triggered when the first instance of the profile is created when we first created a user
    # and in that case we do not have any profile info that we can update the user with!
    if created == False:
        user.username = profile.username
        user.first_name = profile.name
        user.email = profile.email
        user.save()

@receiver(post_delete,sender = Profile)
def deleteUser(sender,instance,**kwargs):
    profile = instance
    user = profile.user
    user.delete()

## we can either use the ones below as signals or decorators above the methods ###
#post_save.connect(createProfile, sender = User)
#post_delete.connect(deleteUser, sender = Profile)
#post_save.connect(updateUser, sender = Profile)