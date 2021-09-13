from os import truncate
from django.db import models
import uuid
from users.models import Profile

# Create your models here


class  Project(models.Model):
    #when   an owner is deleted, we do not want that the projects are deleted because he/she may be done that by accident
    #so when  they come back they still find there projects!
    owner = models.ForeignKey(Profile,null=True, blank=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image =models.ImageField(null=True,blank=True,default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True,blank=True)
    source_link = models.CharField(max_length=2000, null=True,blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0,null=True,blank=True)
    vote_ratio = models.IntegerField(default=0,null=True,blank=True)
    created =  models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True,editable=False)

    def __str__(self):
        return self.title
    class Meta:
        # the dash before created reverse the ordering
        ordering = ['-vote_ratio', '-vote_total','title']

    @property
    def getProjectReviewersIds(self):
        
        #get all the reviewers' Ids of a project, and convert it into a true list!
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property   #so we can use it as an attribute and not as a property without "()"
    def  getVoteCount(self):
        reviews = self.review_set.all()
        upVote = reviews.filter(value = 'up').count()
        totalVotes = reviews.count()
        ratio = int((upVote/totalVotes) * 100) 
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

class Review(models.Model):
    Vote_Type = (
        ('up','Up Vote'),
        ('down','Down Vote')

    )
    owner = models.ForeignKey(Profile,null=True, on_delete=models.CASCADE,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    value = models.CharField(max_length=200,choices=Vote_Type)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True,editable=False)
    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created =  models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True, primary_key=True,editable=False)
    def __str__(self):
        return self.name