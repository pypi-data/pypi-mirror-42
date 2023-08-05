from django.db import models


class Task(models.Model):
    """Task model used to define tasks that will be run as cron jobs """

    name = models.CharField(max_length=255, help_text='The human readable name of the task')
    registered_task = models.ForeignKey('sidekick.RegisteredTask', on_delete=models.CASCADE)
    cron_schedule = models.ForeignKey('sidekick.CronSchedule', on_delete=models.DO_NOTHING)
    enabled = models.BooleanField(default=False, help_text='Whether the task is enabled')

    def __str__(self):
        return self.name

    def task_of(self):
        """The app which this task belongs to """
        return self.registered_task.task_name.split(' ')[0]


class CronSchedule(models.Model):
    """Cron Schedule model for defining different time intervals """

    name = models.CharField(max_length=100, help_text='Human readable version of schedule, i.e Every 10 minutes')
    minute = models.CharField(max_length=100, help_text='At what minute. * for every', default='*')
    hour = models.CharField(max_length=100, help_text='At what hour. * for every', default='*')
    day_of_week = models.CharField(max_length=100, help_text='At what day of the week. * for every', default='*')
    day_of_month = models.CharField(max_length=100, help_text='At what day of the month. * for every', default='*')
    month_of_year = models.CharField(max_length=100, help_text='At what month of the year. * for every', default='*')

    def __str__(self):
        return self.name

    def schedule(self):
        return "{} {} {} {} {}".format(self.minute, self.hour, self.day_of_month, self.month_of_year, self.day_of_week)


class RegisteredTask(models.Model):
    """Model for the registered task to be used by the Task Model """

    task_name = models.CharField(max_length=125, help_text='The task to be run ie. stock --get_stock_updates')

    def __str__(self):
        return self.task_name.replace('--', ' - ').replace('_', ' ')
