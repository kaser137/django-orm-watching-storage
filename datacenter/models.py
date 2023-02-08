import datetime
from django.db import models
from django.utils.timezone import localtime


def get_duration(visit):
  time_zone = datetime.timezone(datetime.timedelta(hours=3))
  duration = localtime(visit.leaved_at) - visit.entered_at.astimezone(time_zone)
  return duration

def format_duration(duration):
  seconds = duration.total_seconds()
  hours = int(seconds // 3600)
  minutes = int((seconds % 3600) // 60)  
  format_duration = f'{hours}h {minutes}min'
  return format_duration

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
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

  
    def is_visit_long(self, minutes=60):
      if self.leaved_at:
        duration = self.leaved_at - self.entered_at
      else:
        duration = localtime() - self.entered_at
      if duration.seconds > minutes*60:
        return True
      return False 

      
    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
