from rest_framework import serializers
from user.models import User



class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = "__all__"
        exclude = ("password",)

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "username", "email", "first_name", "last_name", "is_active"]
