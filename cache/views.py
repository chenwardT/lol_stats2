import logging

from django.http import JsonResponse, HttpResponseBadRequest

# from .summoners import SingleSummoner
from summoners.models import Summoner
from utils.functions import multi_task_status

logger = logging.getLogger(__name__)


def task_status(request):
    # logger.debug(request.POST)
    logger.debug(request.POST.getlist('task_ids[]'))

    # Append [] to refer to a list sent by jQuery.
    if request.is_ajax():
        if 'task_ids[]' in request.POST:
            task_ids = request.POST.getlist('task_ids[]')
            return JsonResponse({'success': multi_task_status(task_ids)})
        else:
            return HttpResponseBadRequest
    else:
        return HttpResponseBadRequest


def is_summoner_refreshable(request):
    logger.debug(request.POST)

    if request.is_ajax() and 'pk' in request.POST:
        pk = request.POST['pk']
        return JsonResponse({'refreshable': Summoner.objects.get(pk=pk).is_refreshable()})
    else:
        return HttpResponseBadRequest
