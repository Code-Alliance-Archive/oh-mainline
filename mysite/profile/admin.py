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

from mysite.profile.models import Person, DataImportAttempt, Tag, TagType, PortfolioEntry, Citation, FormAnswer, \
    FormQuestion, FormResponse
from django.contrib import admin
from mysite.account.models import WelcomeEmailTemplate

admin.site.register(Person)
admin.site.register(DataImportAttempt)
admin.site.register(Tag)
admin.site.register(TagType)
admin.site.register(PortfolioEntry)
admin.site.register(Citation)
admin.site.register(WelcomeEmailTemplate)

class FormAnswerAdmin(admin.ModelAdmin):
    model = FormAnswer
    list_display = ('id','question', 'value')
    search_fields = ('value',)

class FormQuestionAdmin(admin.ModelAdmin):
    model = FormQuestion
    list_display = ('name', 'type', 'required')
    search_fields = ('display_name',)

class FormResponseAdmin(admin.ModelAdmin):
    model = FormResponse
    list_display = ('question','person', 'value')
    search_fields = ('person',)

admin.site.register(FormQuestion, FormQuestionAdmin)
admin.site.register(FormResponse, FormResponseAdmin)
admin.site.register(FormAnswer, FormAnswerAdmin)