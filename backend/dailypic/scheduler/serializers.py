from django_celery_beat.models import PeriodicTask, CrontabSchedule
from rest_framework import serializers

class CrontabScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrontabSchedule
        fields = ['minute', 'hour', 'timezone']

class PeriodicTaskSerializer(serializers.ModelSerializer):
    crontab = CrontabScheduleSerializer()

    class Meta:
        model = PeriodicTask
        fields = ['name', 'task', 'crontab', 'args']

