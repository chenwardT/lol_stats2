import inflection

from celery.result import AsyncResult, GroupResult


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]


# TODO: Compare speed to try/except KeyError block.
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


def multi_task_status(task_ids):
    """
    Returns True if and only if all task were successful, otherwise False.
    """
    return False not in map(lambda task_id: AsyncResult(task_id).successful(), task_ids)


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
