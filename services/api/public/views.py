from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from services.api.public.serializers import ServicesSerializer
from services.models import Service


# Create your views here.
class ServicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.filter(is_active=True).order_by('title')
    serializer_class = ServicesSerializer
    permission_classes = (AllowAny,)
