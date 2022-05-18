from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    created_at      = models.DateTimeField(
        verbose_name= 'created at',
        blank       = True, 
        null        = True, 
        auto_now_add= True
    )
    updated_at      = models.DateTimeField(
        verbose_name= 'updated at',
        blank       = True, 
        null        = True,
        auto_now    = True
    )

    class Meta:
        abstract    = True

class GetRequestLog(models.Model):
    endpoint        = models.CharField(max_length=100, null=True, db_index=True)
    user            = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    response_code   = models.PositiveSmallIntegerField()
    remote_address  = models.CharField(max_length=20, null=True)
    exec_time       = models.IntegerField(null=True)
    date            = models.DateTimeField(auto_now=True, db_index=True)
    body_response   = models.TextField()
    body_request    = models.TextField()

    class Meta:
        db_table    = 'core_get_logs'
        ordering    = ['-date']

    def __str__(self):
        return f'{self.date} | {self.endpoint}'