from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import Resource, Archive
from .serializers import ResourceSerializer, ArchiveSerializer


class ResourceViewset(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    @action(detail=True, methods=["get"])
    def archive(self, request, pk=None):
        resource = get_object_or_404(Resource, pk=pk)
        archive = (
            Archive.objects.filter(resource=resource, status="complete")
            .order_by("created_at")
            .values()
        )
        return Response(
            {
                "archive": archive,
            },
            status=200,
        )
