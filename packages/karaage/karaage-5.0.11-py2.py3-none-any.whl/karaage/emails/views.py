# Copyright 2010-2017, The University of Melbourne
# Copyright 2010-2017, Brian May
#
# This file is part of Karaage.
#
# Karaage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Karaage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Karaage  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import messages
from django.core.mail import send_mass_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from karaage.common.decorators import admin_required
from karaage.emails.forms import BulkEmailForm


@admin_required
def send_email(request):

    form = BulkEmailForm(request.POST or None)
    if request.method == 'POST':

        if form.is_valid():
            if 'preview' in request.POST:
                emails = form.get_emails()
                try:
                    preview = emails[0]
                except IndexError:
                    pass
            else:
                send_mass_mail(form.get_emails())
                messages.success(request, "Emails sent successfully")

                return HttpResponseRedirect(reverse('index'))

    return render(
        template_name='karaage/emails/send_email_form.html', context=locals(),
        request=request)
