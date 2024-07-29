from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Posts(models.Model):
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=200)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to="image1",null=True,blank=True)
    like=models.ManyToManyField(User,related_name="post")

    @ property
    def like_count(self):
        return self.like.all().count()
    @property
    def post_comments(self):
        return Comments.objects.filter(post=self)
    
   
    def __str__(self):
        return self.title
    

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    profile_pic=models.ImageField(upload_to="image1",null=True,blank=True)
    bio=models.CharField(max_length=200)
    time_line_pic=models.ImageField(upload_to="image1",null=True,blank=True)
    nationality = models.CharField(max_length=100, null=True, blank=True)  
    date_of_birth = models.DateField(null=True, blank=True)  
    followers = models.ManyToManyField(User, related_name="following", blank=True)

    def __str__(self):
        return self.user.username

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.user.following.all().count()

class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Posts,on_delete=models.CASCADE)
    comment=models.CharField(max_length=250)
    created_date=models.DateTimeField(auto_now_add=True)
    like=models.ManyToManyField(User,related_name="comment")

    @ property
    def comment_like_count(self):
        return self.like.all().count()
    
    




    