# This file is part of OpenHatch.
# Copyright (C) 2009 OpenHatch, Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db import models
from tinymce.models import HTMLField

class InvitationRequest(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    """Possible other fields:
    - What open source projects are you involved with?
    - What do you wish were better or easier about open source?
    - "Free software" or "Open source"?"""

class WelcomeEmailTemplate(models.Model):
    referring_url = models.URLField(blank=True, max_length=2048, unique=True)
    subject = models.CharField(max_length=998)
    body = HTMLField()

    def __unicode__(self):
        if (not self.referring_url):
            text = 'default'
        else:
            text = self.referring_url
        return text
