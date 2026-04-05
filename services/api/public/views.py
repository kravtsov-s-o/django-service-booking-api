from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from services.api.public.serializers import ServicesSerializer
from services.models import Service


# Create your views here.
@extend_schema(tags=["Public: Services"])
class ServicesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public service catalogue.

    Provides read-only access to active services available for booking.
    """

    queryset = Service.objects.filter(is_active=True).order_by("title")
    serializer_class = ServicesSerializer
    permission_classes = (AllowAny,)
