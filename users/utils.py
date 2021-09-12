# here I can put the reusable functions
#that will be reused in several places in my code
#for example the search function
from django.db.models import Q
from.models import Profile, Skill
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginateProfile(request,profiles, results):
    #which page did we click on? one way to do it:
        # if request.GET.get('page'):
        #     page = request.GET.get('page')
        # else:
        #     page = 1
    #onther way to do it (the same logic expressed differently):
    page = request.GET.get('page')
    #we want to show 3 results per page
    #results = 3
    # creat a Paginator object which which takes as parameter Objects
    #we want to display, and the number of theses objects we want to display per page
    paginator = Paginator(profiles, results)
    try: 
        #here we indicate which page we want to show its objects now and we check
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1

    except EmptyPage:
        #this will give us the total number of pages 
        #if we give it as a parameter for p.page(p.num_pages)
        #it will give us the last page number
        #so if some one call a page that is not in the range  we will render the last page 
        #still if number page is 0 it will send us to the last page
        #we can leave it like this or do an if statement 
        if page == '0':
            page = 1
        else:
            page = paginator.num_pages

    #here we indicate which page we want to show its objects now
    profiles = paginator.page(page)
    #creating a rolling pagination buttons
    #no more than 5 navigation buttons are shown
    leftIndex = (int(page) - 5)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1

    #now we do not loop through all the paginator range but 
    #through the custom index once at a time
    customRange = range(leftIndex,rightIndex)
    return customRange, profiles

def searchProfiles(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains = search_query )
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains = search_query) | 
        Q(short_intro__icontains = search_query)|
        Q(skill__in = skills))

    return profiles, search_query

