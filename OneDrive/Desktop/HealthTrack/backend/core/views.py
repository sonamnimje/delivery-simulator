from django.shortcuts import render
from rest_framework import viewsets
from .models import Workout, Meal, Sleep, Hydration, MedicalHistory
from .serializers import WorkoutSerializer, MealSerializer, SleepSerializer, HydrationSerializer, MedicalHistorySerializer

# Create your views here.

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class SleepViewSet(viewsets.ModelViewSet):
    queryset = Sleep.objects.all()
    serializer_class = SleepSerializer

class HydrationViewSet(viewsets.ModelViewSet):
    queryset = Hydration.objects.all()
    serializer_class = HydrationSerializer

class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
