from django.urls import path
from .views import session_view

urlpatterns = [
  path('session/', session_view),
  path('session/<uuid:id>/', session_view)
]