from django.contrib import admin
from meeting_app.models import Event, Email, Timespan, Option, UsersTimeSpan, UsersOptions, UserEvent

# Register your models here.
admin.site.register(Event)
admin.site.register(Email)
admin.site.register(Timespan)
admin.site.register(Option)
admin.site.register(UsersTimeSpan)
admin.site.register(UsersOptions)
admin.site.register(UserEvent)
