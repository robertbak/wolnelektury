# -*- coding: utf-8 -*-
# This file is part of Wolnelektury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import time
from StringIO import StringIO
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from PIL import Image

from sorl.thumbnail.fields import ImageWithThumbnailsField
from sponsors.fields import JSONField
from django.core.files.base import ContentFile

THUMB_WIDTH=120
THUMB_HEIGHT=120

class Sponsor(models.Model):
    name = models.CharField(_('name'), max_length=120)
    _description = models.CharField(_('description'), blank=True, max_length=255)
    logo = ImageWithThumbnailsField(
        _('logo'),
        upload_to='sponsorzy/sponsor/logo',
        thumbnail={
            'size': (THUMB_WIDTH, THUMB_HEIGHT),
            'extension': 'png',
            'options': ['pad', 'detail'],
        })
    url = models.URLField(_('url'), blank=True, verify_exists=False)

    def __unicode__(self):
        return self.name

    def description(self):
        if len(self._description):
            return self._description
        else:
            return self.name


class SponsorPage(models.Model):
    name = models.CharField(_('name'), max_length=120)
    sponsors = JSONField(_('sponsors'), default={})
    _html = models.TextField(blank=True, editable=False)
    sprite = models.ImageField(upload_to='sponsorzy/sprite', blank=True)

    def populated_sponsors(self):
        result = []
        offset = 0
        for column in self.get_sponsors_value():
            result_group = {'name': column['name'], 'sponsors': []}
            sponsor_objects = Sponsor.objects.in_bulk(column['sponsors'])
            for sponsor_pk in column['sponsors']:
                try:
                    result_group['sponsors'].append((offset, sponsor_objects[sponsor_pk]))
                    offset -= THUMB_HEIGHT
                except KeyError:
                    pass
            result.append(result_group)
        return result

    def render_sprite(self):
        sponsor_ids = []
        for column in self.get_sponsors_value():
            sponsor_ids.extend(column['sponsors'])
        sponsors = Sponsor.objects.in_bulk(sponsor_ids)
        sprite = Image.new('RGBA', (THUMB_WIDTH, len(sponsors)*THUMB_HEIGHT))
        for i, sponsor_id in enumerate(sponsor_ids):
            simg = Image.open(sponsors[sponsor_id].logo.thumbnail.dest)
            sprite.paste(simg, (0, i*THUMB_HEIGHT))
        imgstr = StringIO()
        sprite.save(imgstr, 'png')

        if self.sprite:
            self.sprite.delete(save=False)
        self.sprite.save('sponsorzy/sprite/%s-%d.png' % (self.name, time.time()), ContentFile(imgstr.getvalue()), save=False)

    def html(self):
        return self._html
    html = property(fget=html)

    def save(self, *args, **kwargs):
        self.render_sprite()
        self._html = render_to_string('sponsors/page.html', {
            'sponsors': self.populated_sponsors(),
            'page': self
        })
        return super(SponsorPage, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

