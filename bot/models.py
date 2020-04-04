from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.IntegerField(unique=True, primary_key=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        app_label = 'bot.models.User'


class Message(models.Model):
    update_id = models.IntegerField(unique=True)
    text = models.TextField(max_length=4096)
    date = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        app_label = 'bot.models.Message'


class Statistic(models.Model):
    country = models.TextField
    cases_new = models.IntegerField
    cases_critical = models.IntegerField
    cases_recovered = models.IntegerField
    cases_total = models.IntegerField
    deaths_new = models.IntegerField
    deaths_total = models.IntegerField
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = 'bot.models.Statistic'


class News(models.Model):
    title = models.TextField
    description = models.TextField
    url = models.TextField

    class Meta:
        app_label = 'bot.models.News'
