from django.contrib.auth.models import User
from django.db import models
# from django.contrib.auth.models import AbstractUser


# Create your models here.

# class CustomUser(AbstractUser):
#     email = models.EmailField(unique=True)

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userProfileInfo")
    profile_pic = models.ImageField(upload_to='profile_users', default="images/profile_image.png", blank=True)
    use_google_calendar = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_token")
    token = models.CharField(max_length=100)
    refresh_token = models.CharField(max_length=100)


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    note = models.CharField(max_length=50)
    # This user is creator user
    user = models.ForeignKey(User, related_name='event', on_delete=models.CASCADE, unique=False)
    type = models.CharField(max_length=20, default='case_time_location')
    is_active = models.BooleanField(default=True)

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


class UsersEventCases(models.Model):
    event_cases = models.ForeignKey(EventCases, on_delete=models.CASCADE, related_name='users_event_cases')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_event_cases')


class UserEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='user_event')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_event')

    def __str__(self):
        return str(self.event.title + " _ " + self.user.username)


class FavoriteEvents(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='favorite_events')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_events')

    def __str__(self):
        return str(self.event.title + " _ " + self.user.username)


class ContactUs(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    text = models.TextField(max_length=100)

