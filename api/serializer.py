from rest_framework import serializers
from api.models import Posts
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    date=serializers.DateTimeField(read_only=True)
    user=serializers.CharField(read_only=True)

    class Meta:
        model=Posts
        fields="__all__"


class UserSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
   

    class Meta:
        model=User
        fields=["id","username","password","email","first_name","last_name"]