from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import get_duration
from datacenter.models import format_duration
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    this_passcard_visits = []
    for visit in Visit.objects.filter(passcard=passcard):
      this_passcard_visit = {}
      this_passcard_visit['is_strange']=visit.is_visit_long()
      this_passcard_visit['entered_at']=visit.entered_at.strftime('%d-%m-%Y %H:%M')
      this_passcard_visit['duration']=format_duration(get_duration(visit))
      this_passcard_visits.append(this_passcard_visit)
    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
