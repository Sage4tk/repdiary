from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import User
from .serializer import UserSerializer
# Create your views here.

@api_view(["GET"])
def getUsers(request):

  users  = User.objects.all()

  serialize = UserSerializer(users, many=True)

  return Response({
    'users' : serialize.data
  })

@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def user_views(request):
  # GET USER DATA
  if request.method == "GET":
    serializer = UserSerializer(request.user)
    return Response(serializer)
  
  # EDIT USER
  if request.method == "PUT":
    serializer = UserSerializer(request.user, data=request.data, partial=True)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

