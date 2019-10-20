from django.contrib import admin
from meeting_app.models import Event, Email, UserEvent, EventCases,UsersEventCases, ContactUs, UserToken, FavoriteEvents\
    , UserProfileInfo

# Register your models here.
admin.site.register(Event)
admin.site.register(Email)
admin.site.register(UserEvent)
admin.site.register(EventCases)
admin.site.register(UsersEventCases)
admin.site.register(ContactUs)
admin.site.register(UserToken)
admin.site.register(FavoriteEvents)
admin.site.register(UserProfileInfo)
