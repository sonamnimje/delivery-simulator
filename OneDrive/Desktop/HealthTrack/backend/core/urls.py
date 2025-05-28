from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkoutViewSet, MealViewSet, SleepViewSet, HydrationViewSet, MedicalHistoryViewSet

router = DefaultRouter()
router.register(r'workouts', WorkoutViewSet)
router.register(r'meals', MealViewSet)
router.register(r'sleep', SleepViewSet)
router.register(r'hydration', HydrationViewSet)
router.register(r'medical-history', MedicalHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 