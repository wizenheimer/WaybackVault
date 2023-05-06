from django.urls import path, include
from rest_framework.routers import DefaultRouter
from archive import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"resource", views.ResourceViewset, basename="resource_viewset")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path(
        "resource/<int:pk>/schedule/", views.schedule_archive, name="schedule_archive"
    ),
    path("", include(router.urls)),
]
