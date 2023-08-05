from django.db import models
from django.db.models import fields

from nuntius.models import BaseSubscriber, BaseSegment, BaseSubscriberManager


class TestSegment(BaseSegment, models.Model):
    id = models.CharField(max_length=255, unique=True, primary_key=True)

    def get_display_name(self):
        return self.id

    def get_subscribers_queryset(self):
        return TestSubscriber.objects.filter(segments__id=self.id)

    def get_subscribers_count(self):
        return (
            self.get_subscribers_queryset()
            .filter(subscriber_status=AbstractSubscriber.STATUS_SUBSCRIBED)
            .count()
        )

    def __str__(self):
        return self.get_display_name()


class TestSubscriber(BaseSubscriber):
    objects = BaseSubscriberManager()
    email = fields.EmailField(max_length=255)
    subscriber_status = fields.IntegerField(choices=AbstractSubscriber.STATUS_CHOICES)

    segments = models.ManyToManyField("TestSegment")

    class Meta:
        swappable = "NUNTIUS_SUBSCRIBER_MODEL"
