from django.urls import path
from users.views import SignupView, LoginView, LogoutView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(), name='log-in'),
    path('logout/', LogoutView.as_view(), name='log-out')
]
