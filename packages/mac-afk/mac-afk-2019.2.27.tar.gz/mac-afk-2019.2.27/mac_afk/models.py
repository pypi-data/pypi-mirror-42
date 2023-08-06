#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django
from django.conf import settings
from django.db import models
import os


if not os.path.exists("manage.py") and not settings.configured:
    django.setup()


class Afk(models.Model):
    class Meta:
        app_label = 'mac_afk'
        ordering = ['-created_at']

    created_at = models.DateTimeField(auto_now_add=True)
    seconds = models.IntegerField()

    def __str__(self):
        created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return '<Afk id="%s" created_at="%s" seconds="%s">' % (self.id, created_at, self.seconds)

    def __repr__(self):
        return self.__str__()
