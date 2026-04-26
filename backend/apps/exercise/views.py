import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Session, Exercise
from .serializer import SessionSerializer, ExerciseSerializer
from lib.openai import client
from lib.claude import claude_client
from data.messages import HTTP_500_MESSAGE

# SESSION CRUD VIEW
@api_view([
  'GET',
  'POST',
  'DELETE',
  'PUT'
])
@permission_classes([IsAuthenticated])
def session_view(request, id=None):
  # GET REQUEST
  if request.method == 'GET':
    # IF THERE IS AN ID THEN ONLY GET THE ID
    if id:
      try:
        # CHECK IF PARAMS INCLUDE EXERCISES
        include_exercise = request.query_params.get('include')

        # session = Session.objects.get(id=id)

        # if include_exercise == 'exercises':
        #   session.prefetch_related('exercises').get(id=id)

        if include_exercise == 'exercises':
          session = Session.objects.prefetch_related('exercises').get(id=id)
        else:
          session = Session.objects.get(id=id)

        serializer = SessionSerializer(session, context={'request':request})
        return Response(serializer.data)
      except Session.DoesNotExist:
        return Response({
          'message': 'Session not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # NORMAL FETCH
    # TODO: ADD PAGINATION

    session = Session.objects.all()
    serializer = SessionSerializer(session, many=True)
    return Response(serializer.data)
  
  # CREATE SESSION
  if request.method == 'POST':
    serializer = SessionSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
      serializer.save()

      return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  # DELETE SESSION
  if request.method == "DELETE":
    if not id:
      return Response({'message': 'ID required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      session = Session.objects.get(id=id, user=request.user)
      session.delete()

      return Response({'message': 'Session deleted'}, status=status.HTTP_204_NO_CONTENT)
    except Session.DoesNotExist:
      return Response({'message': "Session not found"}, status=status.HTTP_404_NOT_FOUND)
    
  # EDIT SESSION
  if request.method == "PUT":

    if not id:
      return Response({'message': 'Missing ID'}, status=status.HTTP_400_BAD_REQUEST)

    try:    
      # GET SESSION FIRST
      session = Session.objects.get(id=id, user=request.user)
      serializer = SessionSerializer(session, data=request.data, partial=True, context={'request':request})

      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Session.DoesNotExist:
      return Response({'message': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def exercise_view(request, id=None, session_id=None):
  # CREATE EXERSICE
  if request.method == "POST":
    serializer = ExerciseSerializer(data=request.data)

    # check if valid
    if serializer.is_valid():
      serializer.save()

      return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  # GET ALL EXERCISE FROM SESSION ID
  if request.method == 'GET' and session_id:
    exercises = Exercise.objects.filter(session=session_id)
    serializer = ExerciseSerializer(exercises, many=True)
    
    return Response(serializer.data)
  
  if request.method == "PUT":
    if not id:
      return Response({'message': 'Missing ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      execrise = Exercise.objects.get(id=id)

      serializer = ExerciseSerializer(execrise, data=request.data, partial=True)

      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
      
      return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exercise.DoesNotExist:
      return Response({'message': 'Exercise does not exist'}, status=status.HTTP_404_NOT_FOUND)

  if request.method == 'DELETE':
    if not id:
      return Response({'message': 'ID required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
      exercise = Exercise.objects.get(id=id)
      exercise.delete()

      return Response({ 'message': 'Exercise deleted'}, status=status.HTTP_200_OK)

    except Exercise.DoesNotExist:
      return Response({'message': 'Exercise does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transcribe_exercise(request):
  if request.method == "POST":
    
    # GET AUDIO FILE
    audio_file = request.FILES.get("speech")

    # If no file is found throw error
    if not audio_file:
      return Response({'message':'File not found.'}, status=status.HTTP_400_BAD_REQUEST)

    session_id = request.data.get('session_id')
    if not session_id:
      return Response({'message': 'session_id required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:

      # SEND TO WHISPER API TO TRANSCRIBE
      transcript = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_file
      )

      # SEND TO CLAUDE HAIKU
      response = claude_client.messages.create(
        model='claude-haiku-4-5-20251001',
        max_tokens=1024,
        messages=[
          {
            "role": "user",
            "content": f"""Extract exercises from this transcript and return a JSON array.
Each object must have these fields: exercise, reps, sets, length, notes.
Use null for any field not mentioned.

Transcript: {transcript.text}

Return only a valid JSON array, no explanation."""
          }
        ]
      )

      raw = response.content[0].text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
      exercises_data = json.loads(raw)

      session = Session.objects.get(id=session_id, user=request.user)

      exercises = [Exercise(session=session, **data) for data in exercises_data]
      Exercise.objects.bulk_create(exercises)

      return Response({
        'transcript': transcript.text,
        'created': len(exercises)
      }, status=status.HTTP_201_CREATED)

    except Session.DoesNotExist:
      return Response({'message': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as error:
      print(str(error))
      return Response(
        {
          'message': HTTP_500_MESSAGE
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
      )
    

    


    



