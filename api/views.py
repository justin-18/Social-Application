from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from api.serializer import PostSerializer,UserSerializer
from api.models import Posts
from rest_framework.decorators import action 
from django.contrib.auth.models import User
from rest_framework import authentication,permissions


# Create your views here.
class PostModelViewSet(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=PostSerializer
    queryset=Posts.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


    def list(self,request,*args,**kw):
        qs=Posts.objects.filter(user=request.user)
        serializer=PostSerializer(qs,many=True)
        return Response(data=serializer.data)
        

        
class UserView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()


    # password encrypt
    def create(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            usr=User.objects.create_user(**serializer.validated_data)
            serializer=UserSerializer(usr,many=False)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)