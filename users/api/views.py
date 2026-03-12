from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import ChangePasswordSerializer, MeSerializer


# Create your views here.
@extend_schema(
    tags=["Profile"], summary="Retrieve or update authenticated user profile"
)
class MeView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update the authenticated user's profile.

    GET:
    Return information about the current authenticated user.

    PATCH:
    Update user personal data. Role and permissions cannot be changed.

    Permissions:
    Authenticated users only.
    """

    serializer_class = MeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


@extend_schema(tags=["Profile: Password Reset"], summary="Change user password")
class ChangePasswordView(APIView):
    """
    Change the password of the authenticated user.

    POST:
    Validate the current password and update it with a new one.

    Permissions:
    Authenticated users only.
    """

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
