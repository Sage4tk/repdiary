from rest_framework.response import Response
from rest_framework.decorators import api_view
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