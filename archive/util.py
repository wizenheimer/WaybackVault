import os
import datetime
import requests
from uuid import uuid4
from .models import Archive, Resource
from urllib.parse import urlencode


def get_screenshot(url=None, path=None, folder="media/", filename="screenshot.png"):
    """
    Gets a screenshot using APIFlash
    """
    if path is None:
        path = f"{folder}/{filename}"

    params = {
        "access_key": os.environ.get("API_FLASH_KEY"),
        "url": f"{url}",
        "full_page": True,
        "scroll_page": True,
        "fresh": True,
    }

    url = "https://api.apiflash.com/v1/urltoimage?" + urlencode(params)

    response = requests.get(url)

    with open(f"{path}", "wb") as f:
        f.write(response.content)

    return response.status_code


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
    return f"media/archive/{get_event_id(instance)}.png"


def populate_archive(instance):
    """
    Populates the archive image fields
    """
    url = instance.resource.url
    path = path_generator(instance)

    if get_screenshot(url, path) != 200:
        instance.status = "failed"
    else:
        instance.status = "completed"

    instance.source = path
    instance.save()


def prepare_archive(url=None, date=None):
    """
    Prepares an archive model for the given resource.
    """
    resource = Resource.objects.get_or_create(url=url)[0]
    if date is None:
        date = datetime.datetime.now()
    else:
        date = datetime.strptime(date, "%m-%d-%y %H:%M:%S")

    archive = Archive.objects.get_or_create(
        resource=resource, status="scheduled", created_at=date
    )[0]
    populate_archive(archive)
