# from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import MeSerializer, ChangePasswordSerializer


# Create your views here.
class MeView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update the currently authenticated user.

    GET:
    Returns information about the currently authenticated user.

    PATCH:
    Allows the user to update personal data.
    Role and permissions cannot be changed.

    Access:
    Only available to authenticated users.
    """

    serializer_class = MeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data["current_password"]):
            return Response(
                {"current_password": "Wrong password."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password"])

        return Response({"detail": "Password updated successfully."})
