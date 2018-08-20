from django.db import models

# Create your models here.
from chat.models import TimeStampModel


class ScheduledEvent(TimeStampModel):
    EVENT_TYPE = [
        (1, 'Water Filters'),
        (2, 'Empty Cesspool'),
        (3, 'Other')
    ]

    description = models.CharField(max_length=255)
    event_type = models.SmallIntegerField(choices=EVENT_TYPE)
    color = models.CharField(max_length=10)
