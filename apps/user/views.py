from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from apps.user.models import User
from apps.user.permissions import UserPermission
from apps.user.serializers import UserRegisterSerializer, UserGetMeSerializer


class UserRegisterCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserGetMeApiView(ListAPIView):
    serializer_class = UserGetMeSerializer
    permission_classes = [UserPermission]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return User.objects.filter(id=user.id)
        else:
            return User.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
