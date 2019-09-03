from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_token")
    token = models.CharField(max_length=100)

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    note = models.CharField(max_length=50)
    # This user is creator user
    user = models.ForeignKey(User, related_name='event', on_delete=models.CASCADE, unique=False)

    def __str__(self):
        return self.title


class Email(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="email")

    def __str__(self):
        return str(self.id)


class EventCases(models.Model):
    id = models.AutoField(primary_key=True)
    case_name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_cases")

    def __str__(self):
        return str(self.id)

# class Timespan(models.Model):
#     id = models.AutoField(primary_key=True)
#     start = models.DateTimeField()
#     end = models.DateTimeField()
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="timespan")
#
#     def __str__(self):
#         return str(self.id)
#
#
# class Option(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=20)
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="option")
#
#     def __str__(self):
#         return self.name


# class UsersOptions(models.Model):
#     option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='users_options')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_options')


class UsersEventCases(models.Model):
    event_cases = models.ForeignKey(EventCases, on_delete=models.CASCADE, related_name='users_event_cases')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_event_cases')


class UserEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='user_event')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_event')


class ContactUs(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    text = models.TextField(max_length=100)

