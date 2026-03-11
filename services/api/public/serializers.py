from rest_framework import serializers

from services.models import Service


class ServicesSerializer(serializers.ModelSerializer):
    """
    Serializer representing an active service available to clients.

    Includes basic service information such as title,
    description and base price.
    """
    class Meta:
        model = Service
        fields = (
            "id",
            "title",
            "description",
            "base_price",
        )
