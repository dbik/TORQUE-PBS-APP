from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework import generics, permissions
from rest_framework.response import Response

from models import CustomUser

from serializers import CustomUserSerializer

from permissions import IsOwner


class CustomUserRegistration(generics.CreateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomUserList(generics.ListAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAdminUser,)


class CustomUserDetail(generics.RetrieveUpdateAPIView):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_object(self):
        user_object = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        self.check_object_permissions(self.request, user_object)
        return user_object

    # Need to override update method and set partial to True
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if 'username' in request.data:
            raise PermissionDenied
        if 'email' in request.data:
            raise PermissionDenied
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
