import datetime

from django import template

register = template.Library()


@register.filter
def assign(value):
    data = value
    return data


@register.simple_tag
def update_variable(value):
    """Allows to update existing variable in template"""
    return value


def is_in_time_span(case, list):
    if list:
        for element in list:
            if element.time_span == case:
                return True
    return False


register.filter(is_in_time_span)


def is_in_option(case, list):
    if list:
        for element in list:
            if element.option == case:
                return True
    return False


register.filter(is_in_option)


def best_case(event, users):
    temp = {}
    max = 0
    res = ''
    if event.type == 'time':
        cases = event.timespan.all()
        for case in cases:
            temp[case] = 0
            times = event.user.users_TimeSpan.all()
            for time in times:
                if time.time_span == case:
                    temp[case] = temp[case] + 1
            for user in users:
                times = user.user.users_TimeSpan.all()
                for time in times:
                    if time.time_span == case:
                        temp[case] = temp[case] + 1

        for case, num in temp.items():
            if num >= max:
                res = str(case.start)[:19].replace('-', '/') + "  تا  " + str(case.end)[:19].replace('-','/')
                max = num
    else:
        cases = event.option.all()
        for case in cases:
            temp[case] = 0
            options = event.user.users_options.all()
            for op in options:
                if op.option == case:
                    temp[case] = temp[case] + 1
            for user in users:
                options = user.user.users_options.all()
                for op in options:
                    if op.option == case:
                        temp[case] = temp[case] + 1

        for case, num in temp.items():
            if num >= max:
                res = case.name
                max = num

    return res


register.filter(best_case)
