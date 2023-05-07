from email.policy import default
from operator import index
from typing import Iterable, Optional
from django.db import models


class Resource(models.Model):
    """
    Model for representing a resource, could be a web address
    """

    FREQUENCY_CHOICES = (
        # for development only
        (15, "15 seconds"),
        (60, "1 minute"),
        (180, "3 minutes"),
        (1800, "30 minutes"),
        (6000, "1 hour"),
        # for production usage
        # ("3 hour", "3 hour"),
        # ("6 hour", "6 hour"),
        # ("12 hour", "12 hour"),
        # ("18 hour", "18 hour"),
        # ("1 day", "1 day"),
        # ("1 week", "1 week"),
        # ("1 month", "1 month"),
        # ("3 month", "3 month"),
        # ("6 month", "6 month"),
        # ("12 month", "12 month"),
    )

    # prevent duplicate archive registries
    url = models.URLField(unique=True)
    # frequency of archiving
    frequency = models.PositiveIntegerField(
        default=60,
        choices=FREQUENCY_CHOICES,
    )
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
