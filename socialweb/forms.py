from django import forms
from django.contrib.auth.models import User
from api.models import Posts,UserProfile
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password1","password2"]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))



class ProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=["profile_pic","bio","time_line_pic","nationality","date_of_birth"]


class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","description","image"]
        widgets={
             "title":forms.TextInput(attrs={"class":"form-control"}),
             "description":forms.TextInput(attrs={"class":"form-control"}),
             }


class PostEditForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","description","image"]
        widgets={
             "title":forms.TextInput(attrs={"class":"form-control"}),
             "description":forms.TextInput(attrs={"class":"form-control"}),
              }
        

