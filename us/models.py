from django.db import models
from django.utils.translation import ugettext_lazy as _


class Url(models.Model):
    url = models.TextField(_(u"Url"))
    short_url = models.CharField(_(u"Short URL"), max_length=50, unique=True)

    def __unicode__(self):
        return "{} -> {}".format(self.short_url, self.url)