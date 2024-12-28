from django.urls import path
from animals.views import OnboardedAnimalsView

urlpatterns = [
    path('list/', OnboardedAnimalsView.as_view(), name='onboarded-animals'),
]
