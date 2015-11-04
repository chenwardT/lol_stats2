import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# from .summoners import SingleSummoner
# from summoners.models import standardize_name
from utils.functions import multi_task_status

logger = logging.getLogger(__name__)


# TODO: Remove CSRF exemption.

# @csrf_exempt
# def ajax_summoner_query(request):
#     # logger.debug(request.META)
#     if request.is_ajax():
#         region = request.POST['region'].upper()
#         name = standardize_name(request.POST['name'])
#         logger.debug('region: {}, name: {}'.format(region, name))
#         ss = SingleSummoner(std_name=name, region=region)
#         ss.full_query()
#
#         return JsonResponse({'region': region, 'name': name})
#     else:
#         return JsonResponse({'error': 'error'})
#
#
# @csrf_exempt
# def ajax_is_eligible_for_refresh(request):
#     logger.debug(request.POST)
#
#     if request.is_ajax():
#         region = request.POST['region'].upper()
#         id = request.POST['id']
#
#         logger.debug('region: {}, ID: {}'.format(region, id))
#         ss = SingleSummoner(summoner_id=id, region=region)
#         result = ss.is_cache_fresh()
#         logger.debug('summoner [{}] {} eligible for refresh: {}'
#                      .format(region, id, result))
#
#         return JsonResponse({'result': result})
#     else:
#         return JsonResponse({'error': 'error'})


@csrf_exempt
def task_status(request):
    logger.debug(request.POST.getlist('task_ids[]'))

    if request.is_ajax():
        # Append [] to refer to a list sent by jQuery.
        if 'task_ids[]' in request.POST:
            task_ids = request.POST.getlist('task_ids[]')

            return JsonResponse({'success': multi_task_status(task_ids)})

    return JsonResponse({'error': 'unrecognized request'})