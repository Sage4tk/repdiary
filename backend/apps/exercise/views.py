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
    serializer = SessionSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()

      return Response(serializer.data, status=status.HTTP_201_CREATED)


