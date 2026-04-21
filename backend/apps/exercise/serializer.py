from rest_framework import serializers
from . import models

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

class SessionSerializer(serializers.ModelSerializer):
  exercises = ExerciseSerializer(many=True, read_only=True)

  class Meta:
    model = models.Session
    fields = ['id','title','date', 'created_at', 'exercises']
    read_only_fields = ['user']

  def create(self, validated_data):
    # get user id
    user = self.context['request'].user
    return models.Session.objects.create(user=user, **validated_data)
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    request = self.context.get('request')
    include = request.query_params.get('include') if request else None

    if include != 'exercises':
      self.fields.pop('exercises', None)