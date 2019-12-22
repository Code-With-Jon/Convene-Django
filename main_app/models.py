from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

# class Category:
#     def __init__(self, name):
#       self.name = name

CATEGORIES = (
    ('outdoors', 'Outdoors'),
    ('entertainment', 'Entertainment'),
    ('food', 'Food'),
    ('tech', 'Tech'),
    ('education', 'Education'),
    ('health', 'Health'),
)

class Event(models.Model):
    title = models.CharField(max_length=250)
    date = models.DateField('event date')
    time = models.TimeField('event time')
    location = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    attendees = ArrayField(models.CharField(max_length=250))
    infolink = models.CharField(max_length=1000)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=100,
        choices=CATEGORIES,

    )

    users = models.ManyToManyField(User)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)


    def get_absolute_url(self):
        return reverse('events_detail', kwargs={'event_id': self.id})

    


class Comment(models.Model):
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    created_date = models.DateTimeField(default=timezone.now)
