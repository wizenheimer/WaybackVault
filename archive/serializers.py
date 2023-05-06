from rest_framework import serializers
from .models import Resource, Archive


class ArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archive
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    archive = serializers.SerializerMethodField("fetch_archive", read_only=True)

    class Meta:
        model = Resource
        fields = [
            "url",
            "id",
            "archive",
        ]

    def fetch_archive(self, instance):
        return (
            Archive.objects.filter(resource=instance, status="complete")
            .order_by("created_at")
            .values()
        )
