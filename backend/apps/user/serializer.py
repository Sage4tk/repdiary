from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ['id','first_name', 'last_name', 'email', 'password', 'birth', 'username']

  def create(self, validated_data):
    return User.objects.create_user(**validated_data)