from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.user.serializer import UserSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import LoginSerializer
from apps.user.models import User
import time

@api_view(['POST'])
def register(request):
  # serialize data
  serializer = UserSerializer(data=request.data)
  
  start = time.time()
  if (serializer.is_valid()):

    print("Save took:", time.time() - start)
    user = serializer.save()

    # generate refresh token
    refresh = RefreshToken.for_user(user)

    return Response({
      'access_token': str(refresh.access_token),
      'refresh_token': str(refresh)
    })

  return Response(
    serializer.error_messages,
    status=status.HTTP_400_BAD_REQUEST
  )

@api_view(['POST'])
def login(request):

  # serialize request
  serializer = LoginSerializer(data=request.data)

  if serializer.is_valid():
    
    user = User.objects.filter(id='196f05bd-f991-45ce-97c6-6d39343a7124').first()

    # if user exist create token
    if user:
      print(user.id, user.email)

      refresh = RefreshToken.for_user(user)

      return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
      })

    return Response({
      'message': 'User found',
      'data': str(user)
    })


  return Response({
    'message': 'Something went wrong'
  })