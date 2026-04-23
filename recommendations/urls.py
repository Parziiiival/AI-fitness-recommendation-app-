from django.urls import path
from .views import get_recommendation, get_history, get_insights

urlpatterns = [
    path('predict/', get_recommendation, name='get_recommendation'),
    path('history/', get_history, name='get_history'),
    path('insights/', get_insights, name='get_insights'),
]