import logging

import inflection
from django.apps import apps

from celery.result import AsyncResult, GroupResult

logger = logging.getLogger(__name__)


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


def get_val_or_none(dct, key):
    """
    If `key` exists in dict, return the value of `key` in dict,
    otherwise returns None.

    Used for creating/updating model instances based on Riot DTOs,
    where certain keys are only included in JSON responses if they contain
    a non-zero/-empty value.
    """
    if key in dct:
        return dct[key]
    else:
        return None


def non_dict_or_list_keys(dct):
    """
    Yields keys of dct whose associated values are not of type list or dict.
    """
    for k in dct:
        if not isinstance(dct[k], list) and not isinstance(dct[k], dict):
            yield k


def underscore_dict(dct):
    """
    Returns a copy of dct with top-level keys in camel_case.
    """
    under_dict = {}

    for k in dct:
        under_dict[inflection.underscore(k)] = dct[k]

    return under_dict


# TODO: Ensure task_ids exist and are of type AsyncResult.
def multi_task_status(task_ids):
    """
    Returns True if and only if all task were successful, otherwise False.
    """
    logger.debug('task_ids: {}'.format(task_ids))

    if task_ids:
        return False not in map(lambda task_id: AsyncResult(task_id).successful(), task_ids)
    else:
        return False


def group_status(group_id, result_ids):
    results = [AsyncResult(r_id) for r_id in result_ids]
    gr = GroupResult(id, results)

    return gr.successful()


def coalesce_task_ids(results):
    task_ids = []

    for task in results:
        if isinstance(task, GroupResult):
            for async_result in task.children:
                task_ids.append(async_result.id)
        elif isinstance(task, AsyncResult):
            task_ids.append(task.id)

    return task_ids


def standardize_name(name):
        return name.replace(' ', '').lower()


def is_complete_version(version_str):
    """
    Returns True if a string contains a complete version, like '5.21.0.313'
    otherwise False, like when the string is an incomplete version, e.g. '5.21'.
    """
    return len(version_str.split('.')) == 4

# FIXME: Hack - in prod we would want a better way of getting latest version.
def get_latest_version():
    MatchDetail = apps.get_model('matches', 'MatchDetail')
    return MatchDetail.objects.order_by('match_creation').last().match_version