from django.contrib import admin
from meeting_app.models import Event, Email, UserEvent, EventCases, ContactUs

# Register your models here.
admin.site.register(Event)
admin.site.register(Email)
admin.site.register(UserEvent)
admin.site.register(EventCases)
admin.site.register(ContactUs)
