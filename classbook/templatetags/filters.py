from django.template.defaultfilters import register


@register.filter()
def by_pupil(query_obj, key):
    """ """
    return query_obj.filter(pupil=key)


@register.filter()
def by_date(query_obj, key):
    """ """
    return query_obj.filter(date=key)


@register.filter()
def str_score(query_obj):
    """ """
    if query_obj.count() == 1:
        return query_obj.first().score
    if query_obj.count() > 1:
        return ", ".join([str(qo.score) for i, qo in enumerate(query_obj)])
    return ""


@register.filter()
def id_score(query_obj):
    """ """
    if query_obj.count() == 1:
        return query_obj.first().id
    if query_obj.count() > 1:
        return ", ".join([str(qo.id) for i, qo in enumerate(query_obj)])
    return ""


@register.filter()
def by_lesson(query_obj, key):
    """ """
    return query_obj.filter(lesson=key)


@register.filter()
def str_lesson(query_obj):
    """ """
    if query_obj.count() == 1:
        return query_obj.first().discipline.name


