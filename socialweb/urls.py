from django.urls import path
from socialweb import views

urlpatterns = [
    path("signup",views.SignUpView.as_view(),name="register"),
    path("",views.LoginView.as_view(),name="signin"),
    path("profile/create",views.ProfileCreateView.as_view(),name="profile-create"),
    path("profile",views.ProfileView.as_view(),name="profile-view"),
    path("profile/<int:id>/change",views.ProfileUpdateView.as_view(),name="profile-change"),
    path("home",views.IndexView.as_view(),name="home"),
    path("posts/add",views.PostCreateView.as_view(),name="post-add"),
    path("posts/all",views.PostListView.as_view(),name="post-list"),
    path("posts/details/<int:id>",views.PostDetailView.as_view(),name="post-detail"),
    path("posts/remove/<int:id>",views.PostDeleteView.as_view(),name="post-delete"),
    path("posts/<int:id>/change",views.PostEditView.as_view(),name="post-edit"),
    path("signout",views.LogoutView.as_view(),name="signout"),
    path("posts/<int:pk>/remove",views.PostDeleteView.as_view(),name="post-delete"),
    path("posts/<int:id>/like/add",views.LikeView.as_view(),name="like"),
    path("posts/<int:id>/like/remove",views.LikeRemoveView.as_view(),name="like-remove"),
    path("post/<int:id>/comments/add",views.AddCommentsView.as_view(),name="add-comment"),
    path("comments/<int:pk>/remove",views.CommentsDeleteView.as_view(),name="comment-delete"),
    path("comments/<int:id>/like/add",views.CommentLikeView.as_view(),name="like-comment"),
    path("comments/<int:id>/like/remove",views.CommentLikeRemoveView.as_view(),name="remove-like-remove"),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
   
]