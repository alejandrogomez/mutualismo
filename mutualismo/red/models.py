from django.contrib.auth.models import User as BaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

import datetime


class Category(models.Model):
    name        = models.CharField(_('name'), max_length=124)
    description = models.TextField(_('description'))
    slug        = models.SlugField(_('slug'), unique=True)

    class Meta:
        verbose_name        = _('category')
        verbose_name_plural = _('categories')
        ordering            = ('name',)

    def __unicode__(self):
        return u'%s' % self.name


class SubCategory(Category):
    parent = models.ForeignKey(Category, related_name='sub')


class Trade(models.Model):
    """
    Represents an object or action which can be part of a trade within our network. 
    """
    name        = models.CharField(_('name'), max_length=124)
    description = models.TextField(_('description'))
    # XXX Are we going to allow uncategorized trades? 
    category    = models.ForeignKey(Category)
    # TODO tags

    def __unicode__(self):
        return u'%s' % self.name


class Loan(Trade):
    """
    Represents a good that is available for loan.
    """
    STATUS_CHOICES = (
        (1, _('Available')),
        (2, _('Reserved')),
        (3, _('Not available')),
    )
    status = models.IntegerField(_('status'), choices = STATUS_CHOICES, default = 1)

    class Meta:
        verbose_name = _('loan')
        verbose_name_plural = _('loans')


class Gift(Trade):
    """
    Represents a good that is gifted by its owner.
    """
    communal = models.BooleanField(_('communal'))
    
    class Meta:
        verbose_name = _('gift')
        verbose_name_plural = _('gifts')


class Service(Trade):
    """
    Represents a service that can be offered or demanded.  
    """
    starts       = models.DateTimeField(_('start date'))
    ends         = models.DateTimeField(_('end date'))
    availability = models.TextField(_('availability'))

    class Meta:
        verbose_name = _('service')
        verbose_name_plural = _('services')


class User(BaseUser):
    """
    Extends the ``django.contrib.auth.User`` class to store offers, demands, a
    history of the exchanges and more suitable information.
    """
    offerings = models.ManyToManyField(Trade, related_name='offer')
    demands   = models.ManyToManyField(Trade, related_name='demand')
    location  = models.CharField(max_length=124)


class Exchange(models.Model):
    """
    Represents an exchange between users.
    """
    from_user = models.ForeignKey(User, related_name = 'from')
    to_user   = models.ForeignKey(User, related_name = 'to')
    trade     = models.ForeignKey(Trade)
    date      = models.DateTimeField(_('date'), default = datetime.datetime.now)

    class Meta:
        verbose_name = _('exchange')
        verbose_name_plural = _('exchanges')

    def __unicode__(self):
        # TODO
        return u'exchange'
