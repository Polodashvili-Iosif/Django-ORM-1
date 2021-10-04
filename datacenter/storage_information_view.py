from datacenter.models import Passcard, Visit
from django.shortcuts import render


def storage_information_view(request):
    # Программируем здесь
    non_closed_visits = []
    non_closed_visits_raw = Visit.objects.filter(leaved_at=None)
    for visit in non_closed_visits_raw:
        is_strange = False
        person_visits = Visit.objects.filter(passcard=visit.passcard)
        for person_visit in person_visits:
            if person_visit.is_long:
                is_strange = True
                break
        duration = Visit.format_duration(visit.get_duration())
        non_closed_visits.append({'who_entered': visit.passcard.owner_name,
                                  'entered_at': visit.entered_at,
                                  'duration': duration,
                                  'is_strange': is_strange,
                                  }
                                 )

    context = {
        'non_closed_visits': non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
