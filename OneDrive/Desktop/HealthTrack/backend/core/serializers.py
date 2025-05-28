from rest_framework import serializers
from .models import Workout, Meal, Sleep, Hydration, MedicalHistory

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class SleepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sleep
        fields = '__all__'

class HydrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hydration
        fields = '__all__'

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__' 