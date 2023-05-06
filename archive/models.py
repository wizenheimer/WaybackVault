from django.db import models
from datetime import datetime
from uuid import uuid4


def get_event_id(instance):
    """
    Generates a unique identifier for naming the screenshot
    """
    event_id = instance.created_at.strftime("%Y-%m-%d-%H-%M-%S-") + str(uuid4())
    return event_id


def path_generator(instance):
    """
    Uses event_id and resource_id to generate a unique path
    """
    return f"archive/{instance.resource.id}/{instance.get_event_id()}/"


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

    resource = models.ForeignKey(
        Resource, related_name="archives", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.ImageField(
        upload_to=path_generator, help_text="store the image of the resource"
    )

    def __str__(self):
        return str(self.id)
