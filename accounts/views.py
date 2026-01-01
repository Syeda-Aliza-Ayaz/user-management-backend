from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404


from .utils import has_permission
from .serializers import RegisterSerializer, UserSerializer
from .models import User

# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Logged in successfully"})
        return Response({"error": "Invalid credentials"},status = status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
class SomeProtectedView(APIView):
    def get(self, request):
        if not has_permission(request.user, "can_view_users"):
            return Response(status=403)
        return Response({"data": "allowed"})
    
class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not has_permission(request.user, "can_view_users"):
            return Response({"detail": "Forbidden"}, status=403)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# class DeleteUserView(APIView):
#     permission_classes = [IsAuthenticated]
#     def delete(self, request, user_id):
#         if not has_permission(request.user, "can_delete_users"):
#             return Response({"detail": "Forbidden"}, status=403)
#         user = get_object_or_404(User, id=user_id)
#         user.delete()
#         return Response(status=204)

class DeleteUserView(APIView):
    def delete(self, request, user_id):
        if not has_permission(request.user, "can_delete_users"):
            return Response({"detail": "Permission denied"}, status=403)
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"detail": "User deleted"}, status=204)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)