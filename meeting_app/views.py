import json
import re
import httplib2
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views import View
from googleapiclient.discovery import build
from oauth2client import client
from oauth2client.client import OAuth2WebServerFlow
from meeting import settings
from meeting_app.forms import UserForm, EventForm, ContactUsForm, UserInfoForm
from meeting_app.models import Event, Email, EventCases, UserEvent, UsersEventCases, UserToken

"""
    This class is called when user want to add new event for first time and
     we want to get him permission to have access to user google calendar
"""


class OAuth2CallBack(View):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', False)
        if not code:
            return JsonResponse({'status': 'error, no access key received from Google or User declined permission!'})

        flow = OAuth2WebServerFlow(settings.CLIENT_ID_CALENDAR, settings.CLIENT_SECRET_CALENDAR,
                                   scope='https://www.googleapis.com/auth/calendar',
                                   redirect_uri=settings.REDIRECT_URI_CALENDAR,
                                   access_type='offline',  # This is the default
                                   prompt='consent',
                                   )
        credentials = flow.step2_exchange(code)

        http = httplib2.Http()
        http = credentials.authorize(http)
        credentials_js = json.loads(credentials.to_json())
        access_token = credentials_js['access_token']
        # Store the access token in case we need it again!
        user_token = UserToken(user=request.user, token=access_token, refresh_token=credentials.refresh_token)
        user_token.save()
        return redirect('new_event')

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Only GET requests!')


def google_register_call_back(request):
    # adding event about this user.
    # This 'if' is for understanding that user is registering or log in
    # if user is registering he don't have any object in UserEvent model
    # and if he is registered before, if he is invited to an event there is some object in UserEvent model that is
    # created in 'send_email' def
    is_invited_and_registered_before = False
    if UserEvent.objects.filter(user=request.user).count():
        is_invited_and_registered_before = True

    if not User.objects.filter(username=request.user.username).count():
        emails = Email.objects.all()
        for email in emails:
            if email.email == request.user.email:
                if not is_invited_and_registered_before:
                    user_event = UserEvent(user=request.user, event=email.event)
                    user_event.save()

    return redirect("home")


"""
This method renders home page
"""


def home(request):
    # remove non complete events
    # options = EventCases.objects.all()
    # for op in options:
    #     if op.event.type != 'options':
    #         op.delete()
    # times = Timespan.objects.all()
    # for time in times:
    #     if time.event.type != 'time':
    #         time.delete()
    return render(request, "mainPages/home.html")


"""
This method renders dashboard page
"""


def dashboard(request):
    return render(request, "mainPages/dashboard_page.html", {'user': request.user})


"""
    This method is to change information of user 
"""


def change_user_info(request):
    if request.method == 'POST':
        form = UserInfoForm(data=request.POST)
        form.username = request.user.username
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user.username = form.cleaned_data.get("username")
            user.set_password = form.cleaned_data.get("password1")
            user.first_name = form.cleaned_data.get("first_name")
            user.last_name = form.cleaned_data.get("last_name")
            user.email = form.cleaned_data.get("email")
            user.save()
            return redirect("dashboard")
    else:
        form = UserInfoForm()

    return render(request, 'mainPages/change_user_info.html',
                  {'form': form,})

    # if request.method == 'POST':
    #     return render(request, 'mainPages/change_user_info.html', {'user': request.POST})

        # username = request.POST['username']
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        # user = User.objects.get(pk=request.pk)
        # user.username = username
        # user.first_name = first_name
        # user.last_name = last_name
        # user.save()
        # return redirect('dashboard')
    # else:
    #     return render(request, 'mainPages/change_user_info.html', {'user': request.user, 'form': })


""" 
This method is for user registering
"""


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.save()

            auth_user = authenticate(username=user_form.cleaned_data.get('username'),
                                     password=user_form.cleaned_data.get('password1'))
            login(request, auth_user)

            # adding event about this user
            emails = Email.objects.all()
            for email in emails:
                if email.email == user.email:
                    user_event = UserEvent(user=user, event=email.event)
                    user_event.save()

            return redirect("home")
    else:
        user_form = UserForm()

    return render(request, "registration/register.html",
                  {'user_form': user_form, })


""" 
This method is for contact to us
"""


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(data=request.POST)
        if form.is_valid():
            form = form.save()
            form.save()

            return redirect("home")
    else:
        form = ContactUsForm()

    return render(request, "mainPages/contact_us.html",
                  {'form': form, })


def access_to_google_calendar(request):
    # This 'if' is True when user had get access token before
    if UserToken.objects.filter(user=request.user):
        return redirect('new_event')
    else:
        # Following line is for getting google calendar events of user to show him
        flow = OAuth2WebServerFlow(settings.CLIENT_ID_CALENDAR, settings.CLIENT_SECRET_CALENDAR,
                                   scope='https://www.googleapis.com/auth/calendar',
                                   redirect_uri=settings.REDIRECT_URI_CALENDAR)
        generated_url = flow.step1_get_authorize_url()
        return HttpResponseRedirect(generated_url)


"""
 This method is for create new event
"""


def new_event(request):
    if request.method == 'POST':
        event_form = EventForm(data=request.POST)
        if event_form.is_valid():
            note = event_form.cleaned_data['note']
            title = event_form.cleaned_data['title']
            event = Event(title=title, note=note, user=request.user, is_active=True)
            event.save()
            return redirect('event_cases', pk=event.pk)
    else:
        event_form = EventForm()

    return render(request, 'mainPages/new_event.html', {'event_form': event_form})


"""
    In this function cases of event and emails of event is created
"""


def event_cases(request, pk):
    # Following line is for getting google calendar events of user to show him

    test1 = True
    test2 = True

    token = ''
    try:
        token = request.user.user_token.token
        credentials = client.AccessTokenCredentials(token, 'USER_AGENT')
        service = build('calendar', 'v3', credentials=credentials)
        google_calendar_events = service.events().list(calendarId='primary', singleEvents=True,
                                                       orderBy='startTime').execute()
        google_calendar_events = google_calendar_events.get('items', [])
        google_events_list = []
        for event in google_calendar_events:
            try:
                event = {'title': event['summary'], 'start': event['start']['dateTime'],
                         'end': event['end']['dateTime']}
                google_events_list.append(event)
            except:
                test1 = False
                continue
    except:
        test2 = False
        try:
            credentials = client.GoogleCredentials(
                # technically acces token could be an empty string
                token,
                settings.CLIENT_ID_CALENDAR,
                settings.CLIENT_SECRET_CALENDAR,
                request.user.user_token.refresh_token,
                None,  # this is token_expiry, we can leave it None
                settings.REDIRECT_URI_CALENDAR,
                'USER_AGENT'
            )
            credentials.refresh(httplib2.Http())
            credentials = client.AccessTokenCredentials(credentials.access_token, 'USER_AGENT')
            service = build('calendar', 'v3', credentials=credentials)
            google_calendar_events = service.events().list(calendarId='primary', singleEvents=True,
                                                           orderBy='startTime').execute()
            google_calendar_events = google_calendar_events.get('items', [])
            google_events_list = []
            for event in google_calendar_events:
                try:
                    event = {'title': event['summary'], 'start': event['start']['dateTime'],
                             'end': event['end']['dateTime']}
                    google_events_list.append(event)
                except:
                    test1 = False
                    continue
        except:
            flow = OAuth2WebServerFlow(settings.CLIENT_ID_CALENDAR, settings.CLIENT_SECRET_CALENDAR,
                                       scope='https://www.googleapis.com/auth/calendar',
                                       redirect_uri=settings.REDIRECT_URI_CALENDAR)
            generated_url = flow.step1_get_authorize_url()
            return HttpResponseRedirect(generated_url)

    event = Event.objects.get(pk=pk)
    emails = Email.objects.filter(event=event)
    cases = EventCases.objects.filter(event=event)
    return render(request, 'mainPages/event_cases.html',
                  {'event_pk': pk, 'cases': cases, 'emails': emails, 'google_events': google_events_list,
                   'test1': test1, 'test2': test2})


def add_case(request):
    start_time = request.GET.get("start_time", None)
    end_time = request.GET.get("end_time", None)
    case_name = request.GET.get("case_name", None)
    location = request.GET.get("location", None)
    event_pk = request.GET.get("event_pk", None)
    event = Event.objects.get(pk=event_pk)

    error = ''
    if case_name:
        event_case = EventCases(case_name=case_name, start_time=start_time, end_time=end_time, location=location,
                                event=event)
        event_case.save()
    else:
        error = 'case_name'
    data = {
        'error': error,
    }
    return JsonResponse(data)


"""
This method is called from js file to to remove email of event 
"""


def remove_case(request):
    case_pk = request.GET.get('case_pk', None)
    case = EventCases.objects.get(pk=case_pk)
    case.delete()
    data = {
    }
    return JsonResponse(data)


def user_events(request, pk):
    user = User.objects.get(pk=pk)
    events1 = Event.objects.filter(user=user).all()
    event_user = UserEvent.objects.filter(user=user).all()

    # remove events that have no case to vote
    all_events = Event.objects.all()
    for event in all_events:
        if event.event_cases.count() == 0:
            event.delete()

    id_list = []
    # This 'for' is for events that this user is creator
    if events1:
        for e in events1:
            id_list.append(e.pk)

    # This 'for' is for events that this user is invited
    if event_user:
        for e in event_user:
            id_list.append(e.event.pk)
    events = Event.objects.filter(id__in=id_list).all()
    return render(request, 'mainPages/user_events.html', {'user': user, 'events': events, })


"""
This method is called from js file to to remove email of event 
"""


def remove_email(request):
    email_pk = request.GET.get('email_pk', None)
    email = Email.objects.get(pk=email_pk)
    email.delete()
    data = {
    }
    return JsonResponse(data)


"""
This method is called from js file to to approve comments 
"""


def add_email(request):
    email = request.GET.get('email', None)
    event_pk = request.GET.get('event_pk', None)
    event = Event.objects.get(pk=event_pk)
    event_emails = Email.objects.filter(event=event)

    def is_valid_email(email):
        if len(email) > 7:
            return bool(re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", email))
        return False

    valid = True
    if not is_valid_email(email):
        valid = False

    non_repetitious = True
    for em in event_emails:
        if str(em.email) == str(email):
            non_repetitious = False

    if non_repetitious and valid:
        email = Email(email=email, event=event)
        email.save()

    data = {
        'valid': valid, 'non_repetitious': non_repetitious,
    }
    return JsonResponse(data)


"""
This method is called from js file to to approve comments 
"""


def send_email(request):
    event_pk = request.GET.get('event_pk', None)
    event = Event.objects.get(pk=event_pk)
    test_send_email = True
    check_cases = True
    if event.event_cases.count() == 0:
        check_cases = False
    if check_cases:
        emails = Email.objects.filter(event=event)
        user_registered_emails = []
        user_not_registered_emails = []
        users = User.objects.all()
        for email in emails:
            registered = False
            for user in users:
                if user.email == email.email:
                    registered = True
                    break
            if registered:
                user_registered_emails.append(email.email)
                user = User.objects.get(email=email.email)
                user_event = UserEvent(event=event, user=user)
                user_event.save()
            else:
                user_not_registered_emails.append(email.email)

        text1 = """\
            شما به یک رویداد دعوت شده اید.
            چون تا به حال در این سایت ثبت نام نگرده اید ابتدا از طریق لینک زیر ثبت نام کنید و سپس در بخش داشبورد این رویداد را خواهید دید.
            روی لینک زیر کلیک کنید:\n
            http://127.0.0.1:8000/register
        """
        text2 = """\
            شما به یک رویداد دعوت شده اید.
            از طریق لینک زیر وارد وب سایت شده و در بخش داشبورد رویداد را ببینید.    
            روی لینک زیر کلیک کنید:
            http://127.0.0.1:8000
        """
        try:
            send_mail(
                'رویداد جدید',
                text2,
                'majidad09@gmail.com',
                user_registered_emails
            )
            send_mail(
                'رویداد جدید',
                text1,
                'majidad09@gmail.com',
                user_not_registered_emails
            )
        except:
            test_send_email = False

    data = {
        'test': test_send_email,
        'check_cases': check_cases,
    }
    return JsonResponse(data)


"""
This method is called from js file to to approve comments 
"""


def add_vote(request):
    user_pk = request.GET.get('user_pk', None)
    user = User.objects.get(pk=user_pk)
    voted = False
    event_is_active = False
    # This 'if' is for checking this user that click on button is user in that row of table or not
    if user == request.user:
        test_user = True
        case_pk = request.GET.get('case_pk', None)
        case = EventCases.objects.get(pk=case_pk)
        event = case.event
        if event.is_active:
            event_is_active = True
            if UsersEventCases.objects.filter(user=user, event_cases=case).exists():
                voted = True
                user_case = UsersEventCases.objects.get(user=user, event_cases=case)
                user_case.delete()
            else:
                user_case = UsersEventCases(user=user, event_cases=case)
                user_case.save()

    else:
        test_user = False

    data = {
        'test_user': test_user,
        'voted': voted,
        'event_is_active': event_is_active,
    }
    return JsonResponse(data)


def add_to_google_calendar(request):
    event_pk = request.GET.get('event_pk', None)
    event = Event.objects.get(pk=event_pk)
    event_users = event.user_event.all()

    user_email = []
    for u_e in event_users:
        user_email.append({'email': u_e.user.email})

    # in following code we find best case of event
    best_case = None
    temp = {}
    max = 0
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
                best_case = case
                max = num
    co = 0
    try:
        token = event.user.user_token.token
        co += 1
        credentials = client.AccessTokenCredentials(token, 'USER_AGENT')
        co += 1
        service = build('calendar', 'v3', credentials=credentials)
        co += 1
        new_event = service.events().insert(calendarId='primary',
                                            sendNotifications=True, body={
                'summary': event.title,
                'description': event.note,
                'start': {'dateTime': best_case.start_time.isoformat()},
                'end': {'dateTime': best_case.end_time.isoformat()},
                'attendees': user_email
            }).execute()
        event.is_active = False
        event.save()

        co += 1
    except:
        pass

    user_event = event.user_event.all()
    for u_e in user_event:
        user = u_e.user
        try:
            token = user.user_token.token
            credentials = client.AccessTokenCredentials(token, 'USER_AGENT')
            service = build('calendar', 'v3', credentials=credentials)
            new_event = service.events().insert(calendarId='primary',
                                                sendNotifications=True, body={
                    'summary': event.title,
                    'description': event.note,
                    'start': {'dateTime': best_case.start_time.isoformat()},
                    'end': {'dateTime': best_case.end_time.isoformat()},
                    'attendees': user_email
                }).execute()

        except:
            continue

    data = {}
    return JsonResponse(data)
