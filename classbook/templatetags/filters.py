from django.template.defaultfilters import register
import datetime

days = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']


@register.filter()
def add_weekday(obj, key):
    return str(key) + ", " + days[datetime.date.fromisoformat(str(key)).weekday()]


@register.filter()
def by_pupil(query_obj, key):
    """ """
    return query_obj.filter(pupil=key)


@register.filter()
def by_lesson(query_obj, key):
    """ """
    return query_obj.filter(lesson=key)


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
def by_numb_lesson(query_obj, key):
    """ """
    return query_obj.filter(number=key)


@register.filter()
def by_day(query_obj, key):
    """ """
    data_lesson = query_obj.filter(day=datetime.date.fromisoformat(str(key)).weekday()).first()
    if data_lesson:
        return str(data_lesson.discipline) + ', ' + str(data_lesson.cabinet)
    else:
        return 'нет уроков'
        # return '<text color="gray">нет уроков</text>'

