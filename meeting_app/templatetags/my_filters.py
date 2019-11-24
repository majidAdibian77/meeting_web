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


def is_in_case(case, list):
    if list:
        for element in list:
            if element.event_cases == case:
                return True
    return False


register.filter(is_in_case)


def is_in_favorite(user, list):
    if list:
        for element in list:
            if element.user == user:
                return True
    return False


register.filter(is_in_favorite)


def not_registered_emails(email, event):
    for user_event in event.user_event.all():
        temp_email = user_event.user.email
        if temp_email == email:
            return False
    return True

register.filter(not_registered_emails)


def best_case(event, event_users):
    temp = {}
    max = 0
    res = ''
    cases = event.event_cases.all()
    for case in cases:
        temp[case] = 0
        voteds = event.user.users_event_cases.all()
        for voted in voteds:
            if voted.event_cases == case:
                temp[case] += 1
        for event_user in event_users:
            voteds = event_user.user.users_event_cases.all()
            for voted in voteds:
                if voted.event_cases == case:
                    temp[case] += 1
        for case, num in temp.items():
            if num >= max:
                res = case.case_name
                max = num

    return res


register.filter(best_case)
