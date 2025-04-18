# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "username": user.username,
                "nickname": user.nickname
            }, status=status.HTTP_201_CREATED)
        else:
            if 'username' in serializer.errors:
                return Response({
                    "error": {
                        "code": "USER_ALREADY_EXISTS",
                        "message": "이미 가입된 사용자입니다."
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "token": str(refresh.access_token)
            })
        else:
            return Response({
                "error": {
                    "code": "INVALID_CREDENTIALS",
                    "message": "아이디 또는 비밀번호가 올바르지 않습니다."
                }
            }, status=status.HTTP_401_UNAUTHORIZED)