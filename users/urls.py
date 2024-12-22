from django.urls import path
from users.views import SignupView, LoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(), name='log-in')
]
