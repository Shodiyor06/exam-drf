from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import RegisterSerializer, UserSerializer
from .permissions import IsAdmin
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
