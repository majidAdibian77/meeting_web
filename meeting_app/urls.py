from django.conf.urls import url
from meeting_app import views
from meeting_app.views import OAuth2CallBack

urlpatterns = [
    url(r'^new_event$', views.new_event, name="new_event"),
    url(r'^event_cases/(?P<pk>\d+)$', views.event_cases, name="event_cases"),
    url(r'^access_to_google_calendar$', views.access_to_google_calendar, name="access_to_google_calendar"),
    # url(r'^options_times/(?P<pk>\d+)$', views.options_times, name="options_times"),
    # url(r'^options_times/survey_event/(?P<pk>\d+)$', views.survey_event, name="survey_event"),
    # url(r'^add_time$', vie`ws.add_time, name="add_time"),
    # url(r'^update_time$', views.update_time, name="update_time"),
    # url(r'^remove_time$', views.remove_time, name="remove_time"),
    # url(r'^add_option$', views.add_option, name="add_option"),
    url(r'^remove_case$', views.remove_case, name="remove_case"),
    url(r'^add_email$', views.add_email, name="add_email"),
    url(r'^remove_email$', views.remove_email, name="remove_email"),
    url(r'^add_case$', views.add_case, name="add_case"),
    url(r'^send_email$', views.send_email, name="send_email"),
    url(r'^add_vote$', views.add_vote, name="add_vote"),

    url(r'^oauth2_callback', OAuth2CallBack.as_view(), name='oauth2_callback'),
    url(r'^add_to_google_calendar$', views.add_to_google_calendar, name='add_to_google_calendar'),
    url(r'^add_to_favorite_events$', views.add_to_favorite_events, name='add_to_favorite_events'),
    url(r'^remove_favorite_events$', views.remove_favorite_events, name='remove_favorite_events'),

    url(r'^change_user_info/$', views.change_user_info, name='change_user_info'),
    url(r'^user_favorite_events/$', views.user_favorite_events, name='user_favorite_events'),
    url(r'^user_not_voted_events/$', views.user_not_voted_events, name='user_not_voted_events'),
    url(r'^single_event_user/(?P<pk>\d+)$', views.single_event_user, name='single_event_user'),

    url(r'^add_google_calendar/$', views.add_google_calendar, name='add_google_calendar'),
    ]