from operator import index
from typing import Iterable, Optional
from django.db import models


class Resource(models.Model):
    """
    Model for representing a resource, could be a web address
    """

    # prevent duplicate archive registries
    url = models.URLField(unique=True)
    # frequency of archiving
    frequency = models.PositiveIntegerField(default=1800)
    # last archive date
    last_archived_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    # to deactivate archiving
    is_active = models.BooleanField(default=True)

    # TODO: deactivate invalid links
    # TODO: deactivate links with higher failure rates
    # TODO: deactivate links from archive scheduler
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
        upload_to=f"media/archive/",
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

    def save(self, *args, **kwargs):
        if self.source is not None:
            # register the last archived time
            # TODO: alternative is to create a property which queries this in realtime using archive model
            self.resource.last_archived_at = self.created_at
            self.resource.save()
        super(Archive, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
