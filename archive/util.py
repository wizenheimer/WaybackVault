from uuid import uuid4
from .models import Archive, Resource
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.headless = True


def get_screenshot(url=None, path=None, folder="uploads/", filename="screenshot.png"):
    """
    Gets a screenshot using selenium
    """
    if path is None:
        path = f"{folder}/{filename}"
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    driver.save_screenshot(path)
    driver.quit()


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
    return f"uploads/archive/{get_event_id(instance)}.png"


def populate_archive(instance):
    """
    Populates the archive image fields
    """
    url = instance.resource.url
    path = path_generator(instance)
    instance.status = "failed"
    instance.save()
    get_screenshot(url, path)
    instance.source = path
    instance.status = "complete"
    instance.save()


def archive(url):
    """
    Prepares an archive model for the given resource.
    """
    resource = Resource.objects.get_or_create(url=url)[0]
    archive = Archive.objects.create(resource=resource)
    # TODO: Enqueue the archive to be populated
    populate_archive(archive)
