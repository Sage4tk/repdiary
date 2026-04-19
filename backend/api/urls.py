from django.urls import path, include
from apps.user import views

urlpatterns = [
  path('', views.getUsers),
  path('auth/', include('apps.auth.urls')),
  path('exercise/', include('apps.exercise.urls')),
  path('user/', include('apps.user.urls'))
]