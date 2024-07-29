from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View,UpdateView,CreateView,ListView
from socialweb.forms import UserForm,LoginForm,ProfileForm,PostForm,PostEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from api.models import Posts,UserProfile,Comments
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

decs=[signin_required,never_cache]

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=UserForm()
        return render(request,"register.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"your account has been created successfully")
            return redirect("signin")
        else:
            messages.error(request,"failed to create account")
            return render(request,"register.html",{"form":form})
    

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                return redirect("home")
            else:
                return render(request,"login.html",{"form":form})



class LogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

@method_decorator(decs,name="dispatch")  
class ProfileCreateView(View):
    def get(self,request,*args,**kwargs):
        form=ProfileForm()
        return render(request,"profile-create.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=ProfileForm(request.POST,files=request.FILES)
        if form.is_valid():
            usr=User.objects.get(username=request.user.username)
            form.instance.user=usr
            form.save()
            return redirect("profile-view")
        else:
            return render(request,"profile-create.html",{"form":form})

@method_decorator(decs,name="dispatch")
class ProfileView(View):
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.filter(user=request.user)
        return render(request,"profile1.html",{"profile":qs})

@method_decorator(decs,name="dispatch")   
class ProfileUpdateView(UpdateView):
    model=UserProfile
    form_class=ProfileForm
    template_name="profile-edit.html"
    success_url=reverse_lazy("home")
    pk_url_kwarg="id"

@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    model=Posts
    form_class=PostForm
    template_name="index.html"
    success_url=reverse_lazy("home")
    context_object_name="posts"

    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    
    def get_queryset(self):
        return Posts.objects.all().order_by("-date")
    
@method_decorator(decs,name="dispatch")
class PostCreateView(View):
    def get(self,request,*args,**kwargs):
        form=PostForm()
        return render(request,"post-add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=PostForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("post-list")
        else:
            return render(request,"post-add.html",{"form":form})


@method_decorator(decs,name="dispatch")
class PostListView(View):
    def get(self,request,*args,**kwargs):
        qs=Posts.objects.filter(user=request.user).order_by("-date")
        return render(request,"post-list.html",{"posts":qs})

@method_decorator(decs,name="dispatch") 
class PostDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        qs=Posts.objects.get(id=id)
        return render(request,"post-detail.html",{"posts":qs})


@method_decorator(decs,name="dispatch")
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        Posts.objects.filter(id=id).delete()
        return redirect("post-list")


@method_decorator(decs,name="dispatch")      
class PostEditView(UpdateView):
    model=Posts
    form_class=PostEditForm
    template_name="post-edit.html"
    success_url=reverse_lazy("post-list")
    pk_url_kwarg="id"


@method_decorator(decs,name="dispatch")       
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Posts.objects.get(id=id).delete()
        return redirect("home")
    
@method_decorator(decs,name="dispatch")
class LikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        li=Posts.objects.get(id=id)
        li.like.add(request.user)
        li.save()
        return redirect("home")

@method_decorator(decs,name="dispatch")
class LikeRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        li=Posts.objects.get(id=id)
        li.like.remove(request.user)
        li.save()
        return redirect("home")

@method_decorator(decs,name="dispatch")
class AddCommentsView(View):
    def post(self,request,*args,**kwargs):
        cid=kwargs.get("id")
        post=Posts.objects.get(id=cid)
        usr=request.user
        cmnt=request.POST.get("comment")
        Comments.objects.create(user=usr,post=post,comment=cmnt)
        return redirect("home")
    
@method_decorator(decs,name="dispatch")
class CommentsDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Comments.objects.get(id=id).delete()
        return redirect("home")
    
    def get_queryset(self):
        return Comments.objects.all().order_by("-created_date")
    
@method_decorator(decs,name="dispatch")
class CommentLikeView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        cmn=Comments.objects.get(id=id)
        cmn.like.add(request.user)
        cmn.save()
        return redirect("home")

@method_decorator(decs,name="dispatch")
class CommentLikeRemoveView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        cmn=Comments.objects.get(id=id)
        cmn.like.remove(request.user)
        cmn.save()
        return redirect("home")
    

@method_decorator(decs,name="dispatch")
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user != user_to_follow:
        user_profile = user_to_follow.profile
        user_profile.followers.add(request.user)
    return redirect('profile', user_id=user_to_follow.id)

@method_decorator(decs,name="dispatch")
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    if request.user != user_to_unfollow:
        user_profile = user_to_unfollow.profile
        user_profile.followers.remove(request.user)
    return redirect('profile', user_id=user_to_unfollow.id)