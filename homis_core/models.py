from django.db import models
from django.contrib.auth.models import User


class Message(object):
    INFO = "info"
    ERROR = "error"

    @property
    def is_error(self):
        return str(self.level).lower() == self.ERROR

    def __init__(self, text = None, level = None):
        if level is None:
            level = self.INFO

        self.text = text
        self.level = level

    def __str__(self):
        return self.text


class MessageList(object):
    def __init__(self, messages = None):
        self.messages = []
        if messages is not None:
            self.messages.extend(messages)

    def __len__(self):
        return len(self.messages)

    def __iter__(self):
        return iter(self.messages)

    def append(self, msg):
        if isinstance(msg, basestring):
            self.messages.append(Message(msg))
        else:
            self.messages.append(msg)

    def extend(self, messages):
        self.messages.extend(messages)

    def error(self, message):
        self.append(Message(message, Message.ERROR))

    @classmethod
    def make(self, value = None):
        if value is None:
            return MessageList()
        elif isinstance(value, Message):
            return MessageList([value, ])
        elif isinstance(value, MessageList):
            return value
        else:
            return MessageList(value)


class Person(models.Model):
    user  = models.OneToOneField(User, blank = True, null = True, related_name = "person")

    nick_name  = models.CharField(max_length = 128)
    email = models.EmailField(blank = True)

    account_number = models.IntegerField(blank = True, null = True)
    bank_number    = models.IntegerField(blank = True, null = True)

    def __unicode__(self):
        return unicode(self.nick_name)
