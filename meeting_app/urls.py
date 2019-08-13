from django.conf.urls import url
from meeting_app import views
urlpatterns = [
    url(r'^new_event/$', views.new_event, name="new_event"),
    url(r'^event_type/(?P<pk>\d+)$', views.event_type, name="event_type"),
    url(r'^options_times/(?P<pk>\d+)$', views.options_times, name="options_times"),
    # url(r'^options_times/survey_event/(?P<pk>\d+)$', views.survey_event, name="survey_event"),
    url(r'^remove_email$', views.remove_email, name="remove_email"),
    url(r'^add_email$', views.add_email, name="add_email"),
    url(r'^add_time$', views.add_time, name="add_time"),
    url(r'^update_time$', views.update_time, name="update_time"),
    url(r'^remove_time$', views.remove_time, name="remove_time"),
    url(r'^remove_option$', views.remove_option, name="remove_option"),
    url(r'^add_option$', views.add_option, name="add_option"),
    url(r'^send_email$', views.send_email, name="send_email"),
    url(r'^add_vote$', views.add_vote, name="add_vote"),
    ]