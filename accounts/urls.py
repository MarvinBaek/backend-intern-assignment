# users/urls.py
from django.urls import path
from .views import SignupAPIView, LoginAPIView, MainPageView

urlpatterns = [
    path("signup", SignupAPIView.as_view(), name="signup"),
    path("login", LoginAPIView.as_view(), name="login"),
    path('main', MainPageView.as_view(), name='main-page'),
]
