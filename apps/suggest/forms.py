# -*- coding: utf-8 -*-
# This file is part of Wolnelektury, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django import forms
from django.core.mail import send_mail, mail_managers
from django.core.urlresolvers import reverse
from django.core.validators import email_re
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


from suggest.models import PublishingSuggestion


class SuggestForm(forms.Form):
    contact = forms.CharField(label=_('Contact'), max_length=120, required=False)
    description = forms.CharField(label=_('Description'), widget=forms.Textarea, required=True)


class PublishingSuggestForm(forms.Form):
    contact = forms.CharField(label=_('Contact'), max_length=120, required=False)
    books = forms.CharField(label=_('books'), widget=forms.Textarea, required=False)
    audiobooks = forms.CharField(label=_('audiobooks'), widget=forms.Textarea, required=False)

    def clean(self, *args, **kwargs):
        if not self.cleaned_data['books'] and not self.cleaned_data['audiobooks']:
            msg = _(u"One of these fields is required.")
            self._errors["books"] = self.error_class([msg])
            self._errors["audiobooks"] = self.error_class([msg])
        return super(PublishingSuggestForm, self).clean(*args, **kwargs)

    def save(self, request):
        contact = self.cleaned_data['contact']
        books = self.cleaned_data['books']
        audiobooks = self.cleaned_data['audiobooks']

        suggestion = PublishingSuggestion(contact=contact, books=books,
            audiobooks=audiobooks, ip=request.META['REMOTE_ADDR'])
        if request.user.is_authenticated():
            suggestion.user = request.user
        suggestion.save()

        mail_managers(u'Konsultacja planu wydawniczego na WolneLektury.pl', u'''\
Zgłoszono nową sugestię nt. planu wydawniczego w serwisie WolneLektury.pl.
%(url)s

Użytkownik: %(user)s
Kontakt: %(contact)s

Książki:
%(books)s

Audiobooki:
%(audiobooks)s''' % {
            'url': request.build_absolute_uri(reverse('admin:suggest_suggestion_change', args=[suggestion.id])),
            'user': str(request.user) if request.user.is_authenticated() else '',
            'contact': contact,
            'books': books,
            'audiobooks': audiobooks,
            }, fail_silently=True)

        if email_re.match(contact):
            send_mail(u'[WolneLektury] ' +
                    ugettext(u'Thank you for your suggestion.'),
                    ugettext(u"""\
Thank you for your comment on WolneLektury.pl.
The suggestion has been referred to the project coordinator.""") +
u"""

-- 
""" + ugettext(u'''Message sent automatically. Please do not reply.'''),
                    'no-reply@wolnelektury.pl', [contact], fail_silently=True)
