from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from account.serializers import RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterApi(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(User, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })
