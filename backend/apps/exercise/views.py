from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Session
from .serializer import SessionSerializer

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
        session = Session.objects.get(id=id)
        serializer = SessionSerializer(session)
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





