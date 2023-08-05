from django.db import models
from django.utils.translation import ugettext_lazy as _


class NewsletterSubscription(models.Model):

    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(_('Email address'), unique=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return u"'%s' (%s)" % (self.date_created, self.email)

    
