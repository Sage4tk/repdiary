from rest_framework import serializers
from . import models

class SessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Session
    fields = ['id','date', 'created_at']
    read_only_fields = ['user']

  def create(self, validated_data):
    # get user id
    user = self.context['request'].user
    return models.Session.objects.create(user=user, **validated_data)
    

class ExerciseSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Exercise
    fields = [
      'id',
      'session',
      'exercise',
      'reps',
      'sets',
      'length',
      'notes'
    ]