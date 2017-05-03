import time
from django.db import models


def current_time():
    return int(time.time())


class Request(models.Model):
    remote_addr = models.TextField()
    request_addr = models.TextField()
    request_uri = models.TextField()
    time = models.BigIntegerField(blank=True, default=current_time)
    dangerous = models.NullBooleanField(blank=True, default=False)
