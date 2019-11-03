import json
import os
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
from meeting_app.forms import UserForm, EventForm, ContactUsForm, UserInfoForm, UserProfileInfoForm
from meeting_app.models import Event, Email, EventCases, UserEvent, UsersEventCases, UserToken, UserProfileInfo, \
    FavoriteEvents

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
        if UserToken.objects.filter(user=request.user).count() != 0:
            user_token = UserToken.objects.get(user=request.user)
            user_token.token = access_token
            user_token.refresh_token = credentials.refresh_token
            user_token.save()
            return redirect('new_event')
        else:
            try:
                user_token = UserToken(user=request.user, token=access_token, refresh_token=credentials.refresh_token)
                user_token.save()
                return redirect('new_event')
            except:
                return JsonResponse(
                    {'status': credentials.refresh_token})

    def post(self, request, *args, **kwargs):
        return HttpResponseNotAllowed('Only GET requests!')


"""
    This def is called when user return after register or login with google account
"""


def google_register_call_back(request):
    # adding event about this user.
    # This 'if' is for understanding that user is registering or log in
    # if user is registering he don't have any object in UserEvent model
    # and if he is registered before, if he is invited to an event there is some object in UserEvent model that is
    # created in 'send_email' def
    is_invited_and_registered_before = False
    if UserEvent.objects.filter(user=request.user).count():
        is_invited_and_registered_before = True

    if not UserProfileInfo.objects.filter(user=request.user).count():
        # create profile for this user (necessary in image of user and google access user)
        profile = UserProfileInfo(user=request.user)
        profile.save()

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
This method renders other page
"""


def dashboard(request):
    # if request.method == 'Post':
    #     user = request.user
    #     profile = UserProfileInfo.objects.get(user=user)
    #     if 'profile_pic' in request.FILES:
    #         delete_image_profile(user)
    #         profile.profile_pic = request.FILES['profile_pic']
    #     profile.save()
    #     return redirect('dashboard')
    # profile_form = UserProfileInfoForm()
    return render(request, "mainPages/dashboard_page.html", {'user': request.user, })


"""
    This method is to change information of user 
"""


def change_user_info(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        # user_form.username = request.user.username
        username = request.POST.get("username")
        profile_form = UserProfileInfoForm(data=request.POST)

        # These lines are used when user write old username in changing user info form
        if request.user.username == username:
            del user_form.errors['username']
        email = request.POST.get("email")
        if User.objects.filter(email=email).count():
            if request.user.email != email:
                user_form.add_error('email', "ایمیل وارد شده قبلا ثبت نام کرده است!")

        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.get(pk=request.user.id)
            user.username = username
            user.set_password = user_form.cleaned_data.get("password1")
            user.first_name = user_form.cleaned_data.get("first_name")
            user.last_name = user_form.cleaned_data.get("last_name")
            user.email = email
            user.save()

            profile = UserProfileInfo.objects.get(user=user)
            profile.user = user

            if 'profile_pic' in request.FILES:
                delete_image_profile(user)
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            auth_user = authenticate(username=user.username,
                                     password=user.password)
            login(request, auth_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('dashboard')
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, "mainPages/change_user_info.html",
                  {'user_form': user_form,
                   'profile_form': profile_form})


"""
This method is for delete image of profile that user remove it from database
"""


def delete_image_profile(user):
    img = UserProfileInfo.objects.get(user=user)
    path = img.profile_pic.url[1:]
    if path != 'media/images/profile_image.png':
        if os.path.exists(path):
            os.remove(path)
        img.delete()

    # user_exist = False
    # if request.method == 'POST':
    #     form = UserInfoForm(data=request.POST)
    #     # username = form.fields['username']
    #     # if User.objects.filter(username=username).count():
    #     #     if request.user.username != username:
    #     #         user_exist = True
    #
    #     form.username = request.user.username
    #     if form.is_valid():
    #         user = User.objects.get(pk=request.user.id)
    #         user.username = form.cleaned_data.get("username")
    #         user.set_password = form.cleaned_data.get("password1")
    #         user.first_name = form.cleaned_data.get("first_name")
    #         user.last_name = form.cleaned_data.get("last_name")
    #         user.email = form.cleaned_data.get("email")
    #         user.save()
    #         return redirect("other")
    # else:
    #     form = UserInfoForm()
    # if user_exist:
    #     form.add_error('username', 'This username is used!')

    # return render(request, 'mainPages/change_user_info.html',
    #               {'form': form,})

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
    # return redirect('other')
    # else:
    #     return render(request, 'mainPages/change_user_info.html', {'user': request.user, 'form': })


""" 
This method is for user registering
"""


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        # This line is for when user wrote repetitious email
        if User.objects.filter(email=request.POST.get("email")).count():
            user_form.add_error('email', "ایمیل وارد شده قبلا ثبت نام کرده است!")

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
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
        profile_form = UserProfileInfoForm()

    return render(request, "registration/register.html",
                  {'user_form': user_form,
                   'profile_form': profile_form})


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
    test3 = True
    if request.user.userProfileInfo.use_google_calendar:
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
                    # technically access token could be an empty string
                    None,
                    settings.CLIENT_ID_CALENDAR,
                    settings.CLIENT_SECRET_CALENDAR,
                    request.user.user_token.refresh_token,
                    None,  # this is token_expiry, we can leave it None
                    "https://accounts.google.com/o/oauth2/token",
                    'USER_AGENT'
                )
                http = credentials.authorize(httplib2.Http())
                credentials.refresh(http)

                # credentials.refresh(httplib2.Http())
                # credentials = client.AccessTokenCredentials(credentials.access_token, 'USER_AGENT')

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
    else:
        google_events_list = []
    event = Event.objects.get(pk=   pk)
    emails = Email.objects.filter(event=event)
    cases = EventCases.objects.filter(event=event)
    return render(request, 'mainPages/event_cases.html',
                  {'event_pk': pk, 'cases': cases, 'emails': emails, 'google_events': google_events_list,
                   'test1': test1, 'test2': test2, 'test3': test3})


"""
    This def is to ask user to use his google calendar or not
"""


def add_google_calendar(request):
    use = request.GET.get("use", None)
    if use == 'yes':
        use = True
    else:
        use = False
    profile_user = UserProfileInfo.objects.get(user=request.user)
    profile_user.use_google_calendar = use
    profile_user.save()
    data = {
        'use': use,
    }
    return JsonResponse(data)


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
    This def is for return favorite events of user
"""


def user_favorite_events(request):
    user = request.user
    favorite_events = user.favorite_events.all().order_by()
    user_favorite_events = []
    for f_e in favorite_events:
        user_favorite_events.append(f_e.event)
    # # remove events that have no case to vote
    # all_events = Event.objects.all()
    # for event in all_events:
    #     if event.event_cases.count() == 0:
    #         event.delete()
    return render(request, 'mainPages/user_favorite_events.html', {'user': user, 'events': user_favorite_events, })

"""
    This def is for return events of user that doesn't vote
"""


def user_not_voted_events(request):
    user = request.user
    events = []
    for u_e in user.user_event.all().reverse():
        events.append(u_e.event)
    not_voted = []
    for event in events:
        voted = False
        for event_case in event.event_cases.all():
            for u_c in event_case.users_event_cases.all():
                if u_c.user == user:
                    voted = True
                    break
        if not voted:
            not_voted.append(event)

    # # remove events that have no case to vote
    # all_events = Event.objects.all()
    # for event in all_events:
    #     if event.event_cases.count() == 0:
    #         event.delete()

    return render(request, 'mainPages/user_not_voted_events.html', {'user': user, 'events': not_voted, })


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

    if email == event.user.email:
        user_email = True
    else:
        user_email = False
    if non_repetitious and valid and not user_email:
        email = Email(email=email, event=event)
        email.save()

    data = {
        'valid': valid,
        'non_repetitious': non_repetitious,
        'user_email': user_email,
    }
    return JsonResponse(data)


"""
This method is called from js file to to approve comments 
"""


def send_email(request):
    event_pk = request.GET.get('event_pk', None)
    event = Event.objects.get(pk=event_pk)
    # These lines are for setting type of event

    cases = event.event_cases.all()
    time = ''
    case_name = ''
    location = ''
    time_test = True
    case_name_test = True
    location_test = True

    for case in cases:
        if not time:
            time = str(case.start_time) + ' ' + str(case.end_time)
        if not case_name:
            case_name = case.case_name
        if not location:
            location = case.location

        if str(case.start_time) + ' ' + str(case.end_time) != time:
            time_test = False
        if case.case_name != case_name:
            case_name_test = False
        if case.location != location:
            location_test = False

    if time_test:
        if location_test:
            type = 'case'
        else:
            if case_name_test:
                type = 'location'
            else:
                type = 'case_location'
    else:
        if location_test:
            if case_name_test:
                type = 'time'
            else:
                type = 'case_time'
        else:
            if case_name_test:
                type = 'time_location'
            else:
                type = 'case_time_location'
    event.type = type
    event.save()

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
            http://127.0.0.1:8000/single_event_user/{}
        """.format(event_pk)
        try:
            send_mail(
                'رویداد جدید',
                text2,
                'ivade@ivade.ir',
                user_registered_emails
            )
            send_mail(
                'رویداد جدید',
                text1,
                'ivade@ivade.ir',
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

    # This 'if' is for checking this user that click on button is user in that row of table or not
    case_pk = request.GET.get('case_pk', None)
    case = EventCases.objects.get(pk=case_pk)
    event = case.event
    event_pk = event.pk

    voted = False
    test_user = False
    if event.is_active:
        event_is_active = True
        if user == request.user:
            test_user = True
            if UsersEventCases.objects.filter(user=user, event_cases=case).exists():
                voted = True
                user_case = UsersEventCases.objects.get(user=user, event_cases=case)
                user_case.delete()
            else:
                user_case = UsersEventCases(user=user, event_cases=case)
                user_case.save()
    else:
        event_is_active = False

    data = {
        'test_user': test_user,
        'voted': voted,
        'event_is_active': event_is_active,
        'event_pk': event_pk,
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
        try:
            credentials = client.GoogleCredentials(
                # technically access token could be an empty string
                None,
                settings.CLIENT_ID_CALENDAR,
                settings.CLIENT_SECRET_CALENDAR,
                event.user.user_token.refresh_token,
                None,  # this is token_expiry, we can leave it None
                "https://accounts.google.com/o/oauth2/token",
                'USER_AGENT'
            )
            http = credentials.authorize(httplib2.Http())
            credentials.refresh(http)

            # credentials.refresh(httplib2.Http())
            # credentials = client.AccessTokenCredentials(credentials.access_token, 'USER_AGENT')

            service = build('calendar', 'v3', credentials=credentials)
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
        except:
            event.is_active = False
            event.save()

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
            try:
                credentials = client.GoogleCredentials(
                    # technically access token could be an empty string
                    None,
                    settings.CLIENT_ID_CALENDAR,
                    settings.CLIENT_SECRET_CALENDAR,
                    user.user_token.refresh_token,
                    None,  # this is token_expiry, we can leave it None
                    "https://accounts.google.com/o/oauth2/token",
                    'USER_AGENT'
                )
                http = credentials.authorize(httplib2.Http())
                credentials.refresh(http)

                # credentials.refresh(httplib2.Http())
                # credentials = client.AccessTokenCredentials(credentials.access_token, 'USER_AGENT')

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
                pass

    data = {}
    return JsonResponse(data)


def add_to_favorite_events(request):
    event_pk = request.GET.get('event_pk', None)
    event = Event.objects.get(pk=event_pk)
    try:
        favorite_events = FavoriteEvents(event=event, user=request.user)
        favorite_events.save()
        test = True
    except:
        test = False
    data = {
        'test': test
    }
    return JsonResponse(data)


def remove_favorite_events(request):
    event_pk = request.GET.get('event_pk', None)
    event = Event.objects.get(pk=event_pk)
    try:
        favorite_events = FavoriteEvents.objects.get(event=event, user=request.user)
        favorite_events.delete()
        test = True
    except:
        test = False
    data = {
        'test': test
    }
    return JsonResponse(data)


def single_event_user(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'mainPages/user_favorite_events.html', {'user': request.user, 'event': event, })

