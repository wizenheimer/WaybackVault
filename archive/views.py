import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from .models import Resource, Archive
from .serializers import ResourceSerializer, ArchiveSerializer
from .tasks import build_archive


# TODO: add support for timezones
class ResourceViewset(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

    @action(detail=True, methods=["get"])
    def archive(self, request, pk=None):
        status = request.query_params.get("status", "completed")
        if status not in ["completed", "scheduled", "failed"]:
            status = "completed"
        resource = get_object_or_404(Resource, pk=pk)
        archive = (
            Archive.objects.filter(resource=resource, status=status)
            .order_by("-created_at")
            .values()
        )
        return Response(
            {
                "archive": archive,
            },
            status=200,
        )


@api_view(["POST"])
def archive_now(request, pk=None):
    date = request.data.get("date", None)
    resource = get_object_or_404(Resource, pk=pk)

    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.strptime(date, "%m-%d-%y %H:%M:%S")

    archive = Archive.objects.get_or_create(
        resource=resource, status="scheduled", created_at=date
    )[0]

    build_archive.send(pk=archive.id)
    return Response(
        {
            "message": "task scheduled successfully.",
        }
    )
