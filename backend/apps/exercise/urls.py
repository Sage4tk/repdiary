from django.urls import path
from .views import session_view, exercise_view, transcribe_exercise

urlpatterns = [
  path('session/', session_view),
  path('session/<uuid:id>/', session_view),
  path('session/exercises/<uuid:session_id>/',exercise_view),
  path('exercise/', exercise_view),
  path('exercise/<uuid:id>/', exercise_view),
  path('transcribe/', transcribe_exercise)
]