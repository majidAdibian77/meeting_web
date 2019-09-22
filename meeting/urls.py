"""meeting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from meeting_app import views
from django.contrib.auth import views as djangoView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url('admin/', admin.site.urls),
                  url(r'^$', views.home, name="home"),
                  url('^api/v1/', include('social_django.urls', namespace='social')),
                  url(r'^login/$', djangoView.LoginView.as_view(), name="login"),
                  url(r'^logout/$', djangoView.LogoutView.as_view(), name="logout"),
                  url(r'^register/$', views.register, name='register'),
                  url(r'^google_register_call_back/$', views.google_register_call_back, name='google_register_call_back'),
                  url(r'^contact_us/$', views.contact_us, name='contact_us'),
                  url(r'^options_times/user_events/(?P<pk>\d+)$', views.user_events, name='user_events'),
                  url(r'^dashboard/$', views.dashboard, name='dashboard'),
                  # url(r'^contact_us/$', views.contact_us, name='contact_us'),
                  url(r'', include("meeting_app.urls")),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
