import dramatiq
import datetime
from uuid import uuid4
from django.shortcuts import get_object_or_404
from urllib.parse import urlencode
import requests
import os
from .models import Archive, Resource
from core.celery import app


def build_path(date):
    filename = date.strftime("%Y-%m-%d-%H-%M-%S-") + str(uuid4()) + ".png"
    path = f"media/archive/{filename}"
    return path


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


def exception_profiler(retries_so_far, exception):
    return retries_so_far < 3 and isinstance(exception, requests.exceptions.ReadTimeout)


# @dramatiq.actor(max_retries=3, retry_when=exception_profiler)
@app.task
def build_archive(pk):
    """
    Prepare a current archive for the given resoure id.
    """
    archive = Archive.objects.get(pk=pk)
    url = archive.resource.url
    path = build_path(archive.created_at)
    try:
        if get_screenshot(url, path) != 200:
            archive.status = "failed"
        else:
            archive.status = "completed"
            archive.source = path
    except requests.exceptions.ReadTimeout as errrt:
        archive.status = "failed"
    except requests.exceptions.RequestException as errex:
        archive.status = "failed"
    finally:
        archive.save()


# @dramatiq.actor(max_retries=3, retry_when=exception_profiler)
@app.task
def periodic_archive(seconds=15):
    """
    Prepare an archive for all active resource.
    Uses iterator to lazy load resources
    Other optimizations tried here, requires tweaking model structure
    Use values_list() to retrieve only the URL field
    Use batch processing to limit the number of records retrieved at once
    """
    # use iterator to lazy load resources
    resources = Resource.objects.filter(is_active=True, frequency=seconds).iterator()
    for resource in resources:
        archive = Archive.objects.get_or_create(
            resource=resource, created_at=datetime.datetime.utcnow(), status="scheduled"
        )[0]

        url = resource.url
        path = build_path(archive.created_at)

        try:
            if get_screenshot(url, path) != 200:
                archive.status = "failed"
            else:
                archive.status = "completed"
                archive.source = path
        except requests.exceptions.ReadTimeout as errrt:
            archive.status = "failed"
        except requests.exceptions.RequestException as errex:
            archive.status = "failed"
        finally:
            archive.save()
