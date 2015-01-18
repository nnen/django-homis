from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user  = models.OneToOneField(User, blank = True, null = True, related_name = "person")

    nick_name  = models.CharField(max_length = 128)
    email = models.EmailField(blank = True)

    account_number = models.IntegerField(blank = True, null = True)
    bank_number    = models.IntegerField(blank = True, null = True)

    def __unicode__(self):
        return unicode(self.nick_name)
