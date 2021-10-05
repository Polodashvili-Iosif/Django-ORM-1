import datetime

import pytz
from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def get_duration(visit):
        if visit.leaved_at is None:
            entered_time = localtime(value=visit.entered_at,
                                     timezone=pytz.timezone('Europe/Moscow')
                                     ).replace(tzinfo=None)
            leave_time = datetime.datetime.now()
        else:
            entered_time = visit.entered_at
            leave_time = visit.leaved_at
        seconds_delta = (leave_time - entered_time).total_seconds()
        return seconds_delta

    def format_duration(duration):
        seconds = int(duration % 60)
        minutes = int(duration % 3600 // 60)
        hours = int(duration // 3600)
        return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

    def is_long(visit, minutes=60):
        return visit.get_duration() / 60 > minutes

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved='leaved at '
                   + str(self.leaved_at) if self.leaved_at else 'not leaved'
        )
