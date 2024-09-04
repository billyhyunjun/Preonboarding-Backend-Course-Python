from django.shortcuts import render
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError, TokenBackendError


class TokenObtainPairView(APIView):
    def post(self, request):
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            if serializer.is_valid():
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except TokenError as e:
            # Handle token errors like invalid or expired token
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenBackendError as e:
            # Handle backend errors related to token decoding
            return Response({'detail': 'Token is invalid or expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Handle any other unexpected errors
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email
        })


class RegisterView(APIView):
    print("들어옴")
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("결과", username, password)
        if username and password:
            if User.objects.filter(username=username).exists():
                return Response({'detail': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
            user = User(username=username, password=make_password(password))
            user.save()
            return Response({'detail': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
