from operator import index
from django.db import models


class Resource(models.Model):
    """
    Model for representing a resource, could be a web address
    """

    url = models.URLField()

    def __str__(self):
        return str(self.url)


class Archive(models.Model):
    """
    Model for representing a archive, could be a HTML file, Image file etc.
    """

    STATUS_CHOICES = (
        ("scheduled", "scheduled"),
        ("completed", "completed"),
        ("failed", "failed"),
    )

    resource = models.ForeignKey(
        Resource, related_name="archives", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.ImageField(
        upload_to=f"uploads/archive/",
        help_text="store the image of the resource",
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        default="scheduled",
        db_index=True,
    )

    def __str__(self):
        return str(self.id)
