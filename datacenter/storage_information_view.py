from datacenter.models import Passcard
from datacenter.models import Visit
from datacenter.models import get_duration
from datacenter.models import format_duration
from django.shortcuts import render
from django.utils.timezone import localtime


def storage_information_view(request):
    non_closed_visits = []
    for visit in Visit.objects.filter(leaved_at=None):
      non_closed_visit = {}
      non_closed_visit['who_entered']=visit.passcard.owner_name
      non_closed_visit['is_strange']=visit.is_visit_long()
      non_closed_visit['entered_at']=localtime(visit.entered_at).strftime('%d-%m-%Y %H:%M')
      non_closed_visit['duration']=format_duration(get_duration(visit))
      non_closed_visits.append(non_closed_visit)
    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
