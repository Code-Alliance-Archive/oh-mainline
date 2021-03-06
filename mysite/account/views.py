# This file is part of OpenHatch.
# Copyright (C) 2010 Parker Phinney
# Copyright (C) 2010 Jessica McKellar
# Copyright (C) 2009, 2010 OpenHatch, Inc.
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

# Imports {{{
from numpy.lib._iotools import str2bool
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
import django.contrib.auth
from django.contrib.auth.decorators import login_required
import django.contrib.auth.forms
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
import django_authopenid.views
from django.contrib.auth.models import User, Group
from django.conf import settings
from mysite.base.models import Experience, Organization, Skill, Language
from mysite.profile.models import Person, Cause, Heard_From, TimeToCommit, FormQuestion, FormAnswer, FormResponse, CardDisplayedQuestion, ListDisplayedQuestion, ExportQuestion

from invitation.forms import InvitationKeyForm
from invitation.models import InvitationKey

import urllib
import urllib2
import logging
import json
import uuid
import os

import mysite.base.views
import mysite.base.view_helpers
import mysite.account.forms
from mysite.base.view_helpers import render_response
from mysite.account.view_helpers import clear_user_sessions
import mysite.profile.views
from mysite.settings import MEDIA_ROOT, MEDIA_URL

# FIXME: We did this because this decorator used to live here
# and lots of other modules refer to it as mysite.account.views.view.
# Let's fix this soon.
from mysite.account.models import WelcomeEmailTemplate
from mysite.base.decorators import view, has_group, _has_group
from forms import EditFieldsForm, EditFieldsDisplayedInSearchForm, EditViewTypeForm, EditExportedFieldsForm
import django.contrib.auth.views
from django.template import Template, Context
# }}}

def signup_do(request):
    # {{{
    post = {}
    post.update(dict(request.POST.items()))
    post['password2'] = post.get('password1', '')
    signup_form = mysite.account.forms.UserCreationFormWithEmail(post)
    if signup_form.is_valid():

        user = signup_form.save()


        username = request.POST['username']
        password = request.POST['password1']

        # authenticate and login
        user = django.contrib.auth.authenticate(
                username=username,
                password=password)
        django.contrib.auth.login(request, user)

        # redirect to profile
        return HttpResponseRedirect(
                '/people/%s/' % urllib.quote(username))

    else:
        return mysite.account.views.signup(request, signup_form=signup_form)
    # }}}

def signup(request, signup_form=None):
    if signup_form is None:
        signup_form = mysite.account.forms.UserCreationFormWithEmail()
    return render_response(request, 'account/signup.html', {'form': signup_form})


def signup_request(request):
    try:
        post_json = json.loads(request.POST.get(u'data', []))
        questions_json = post_json['questions']
        referring_url = post_json['referringUrl']

        email = __getFieldValue__(questions_json, u'Email')
        first_name = __getFieldValue__(questions_json, u'First Name')
        last_name = __getFieldValue__(questions_json, u'Last Name')
        if email is None:
            return HttpResponse(status=400)
        exists = Person.objects.filter(user__email__iexact=email).count() > 0
        if exists:
            User.objects.filter(email__iexact=email).update(username=email, email=email, first_name=first_name,
                                                            last_name=last_name)
            user = Person.objects.get(user__email__iexact=email).user
        else:
            user = User.objects.create(username=email, email=email, first_name=first_name, last_name=last_name)
        random_password = User.objects.make_random_password(length=10)
        user.set_password(random_password)
        if not user.groups.filter(name='VOLUNTEER').count() > 0:
            user.groups.add(Group.objects.get(name='VOLUNTEER'))
        user.save()

        person = user.get_profile()
        person.referring_url = referring_url

        answers = dict()
        responses = dict()
        questions = []
        for question in questions_json:
            question_name = question.get(u'label').strip()
            if question_name in ['First Name', 'Last Name', 'Email']:
                continue
            form_question = None
            if question.get(u'inputType') == 'file' and len(question.get(u'responses')) != 0 and question.get(u'responses')[0] != '':
                file_url = question.get(u'responses')[0]
                try:
                    filename = str(file_url).split('/')[-1]
                    new_request = urllib2.Request(settings.SC4G_FILES_URL + filename)
                    new_request.add_header('Authorization', 'Basic %s' % settings.SC4G_BASIC_AUTH_TOKEN)
                    new_response = urllib2.urlopen(new_request)

                    new_file_path = generate_random_file_path(filename)
                    with open(MEDIA_ROOT + '/' + new_file_path, "wb") as file:
                        file.write(new_response.read())
                        file.close()
                    host = mark_safe('%s://%s%s' % (request.is_secure() and 'https' or 'http',
                                                     request.get_host(), MEDIA_URL))
                    question.get(u'responses')[0] = host + new_file_path
                except urllib2.HTTPError as e:
                    if e.code == 404:
                        question[u'responses'] = []

            if FormQuestion.objects.filter(display_name__iexact=question_name).count() > 0:
                FormQuestion.objects.filter(display_name__iexact=question_name) \
                    .update(type=question.get(u'inputType'), required=question.get(u'required'))
                form_question = FormQuestion.objects.get(display_name__iexact=question_name)

            elif FormQuestion.objects.filter(name__iexact=question_name).count() > 0:
                FormQuestion.objects.filter(name__iexact=question_name) \
                    .update(type=question.get(u'inputType'), required=question.get(u'required'),
                            display_name=question_name)
                form_question = FormQuestion.objects.get(display_name__iexact=question_name)

            else:
                form_question = FormQuestion(name=question_name,
                                             display_name=question_name,
                                             type=question.get(u'inputType'),
                                             required=question.get(u'required'))
                form_question.save()
            questions.append(form_question)
            answers[form_question.name] = []
            responses[form_question.name] = []
            for answer in question.get(u'values'):
                answers[form_question.name].append(FormAnswer(question=form_question, value=answer.strip()))
            for response in question.get(u'responses'):
                if len(response) == 0:
                    continue
                responses[form_question.name].append(FormResponse(question=form_question, person=person,
                                                                  value=response.strip()))
        existing_questions = FormQuestion.objects.all()
        for existing_question in existing_questions:
            is_present = False
            for question in questions:
                if question.name  == existing_question.name:
                    is_present = True
            if not is_present:
                existing_question.delete()
        __updateQuestionAnswers__(FormQuestion.objects.all(), answers)
        __updateQuestionResponses__(person, FormQuestion.objects.all(), responses)
    except (Exception, RuntimeError) as e:
        raise e

    send_registration_email(email=email, user=user, hostname=request.get_host(), random_password=random_password)
    response = HttpResponse(status=200)
    response['Access-Control-Allow-Origin'] = '*'
    return response

def save_view(request):
    try:
        person = request.user.get_profile()
        view = request.POST.get('view')
        if view == 'list':
            person.view_list = True
        elif view == 'cards':
            person.view_list = False
        else:
            return HttpResponse(status=400)
        person.save()
        return HttpResponse(status=200)
    except (Exception, RuntimeError) as e:
        return HttpResponse(status=400)

def generate_random_file_path(filename):
    # MEDIA_ROOT is prefixed automatically.
    random_directory = ('volunteer-files/%s/') % uuid.uuid4().hex
    random_directory_path = MEDIA_ROOT + '/' + random_directory
    if not os.path.exists(random_directory_path):
        os.makedirs(random_directory_path)
    return random_directory + filename

def send_registration_email(email, user, hostname, random_password):
    person = user.get_profile()
    email_template = get_email_template(person.referring_url)
    subject = ''.join(email_template.subject.splitlines())
    context = get_context(user, hostname, random_password)
    content = Template(email_template.body).render(context)
    send_message(email, subject, content)

def get_email_template(referring_url):
    email_template_exists = WelcomeEmailTemplate.objects.filter(referring_url=referring_url).count() > 0
    if email_template_exists:
        email_template = WelcomeEmailTemplate.objects.get(referring_url=referring_url)
    else:
        email_template = WelcomeEmailTemplate.objects.get(id=1)
    return email_template

def get_context(user, hostname, random_password):
    return Context({'user': user, 'hostname': hostname, 'random_password': random_password})

def send_message(receiver, subject, content):
    message = django.core.mail.EmailMessage(subject=subject,
                                        body=content,
                                        to=[receiver]
                                        )
    message.content_subtype = "html"
    message.send()

def __getFieldValue__(questions, label):
    for question in questions:
        if question.get(u'label') == label:
            return question.get(u'responses')[0]
    return None

def __updateQuestionAnswers__(questions, answers):
    for question in questions:
        existing_answers = FormAnswer.objects.filter(question__pk__exact=question.id)
        for answer in answers[question.name]:
            if FormAnswer.objects.filter(Q(question__pk__exact=question.id) and Q(value__iexact=answer.value)).count() == 0:
                answer.save()
        for existing_answer in existing_answers:
            is_present = False
            for answer in answers[question.name]:
                if answer.value == existing_answer.value:
                    is_present = True
            if not is_present:
                FormResponse.objects.filter(Q(question__pk__exact=existing_answer.question.id)
                and Q(value__iexact=existing_answer.value)).delete()
                existing_answer.delete()

def __updateQuestionResponses__(person, questions, responses):
    for question in questions:
        question.formresponse_set.get_query_set().filter(person__pk__exact=person.id).delete()
        for response in responses[question.name]:
            response.save()

@login_required
@view
def edit_photo(request, form=None, non_validation_error=False):
    """
    Set or change your profile photo.

    If non_validation_error is True, there was an error outside the scope of
    form validation, eg an exception was raised while processing the photo.
    """
    if form is None:
        form = mysite.account.forms.EditPhotoForm()
    data = mysite.profile.views.get_personal_data(request.user.get_profile())
    data['edit_photo_form'] = form

    if non_validation_error:
        data['non_validation_error'] = True

    return (request, 'account/edit_photo.html', data)

@login_required
def edit_photo_do(request, mock=None):
    person = request.user.get_profile()
    form = mysite.account.forms.EditPhotoForm(request.POST,
                                       request.FILES,
                                       instance=person)

    try:
        # Exceptions can be raised by the photo manipulation libraries while
        # "cleaning" the photo during form validation.
        valid = form.is_valid()
    except Exception, e:
            logging.error("%s while preparing the image: %s"
                          % (str(type(e)), str(e)))
            # Don't pass in the form. This gives the user an empty form and a
            # nice error message, instead of the displaying the details of the
            # error.
            return edit_photo(request, form=None, non_validation_error=True)

    if valid:
        person = form.save()
        person.generate_thumbnail_from_photo()

        return HttpResponseRedirect(
            reverse(mysite.profile.views.display_person_web, kwargs={
                    'user_to_display__id': request.user.id
                    }))
    else:
        return edit_photo(request, form)

def catch_me(request):
    failboat # NameError

@login_required
@view
def settings(request):
    # {{{
    data = {}
    return (request, 'account/settings.html', data)
    # }}}

@login_required
@view
def edit_contact_info(request, edit_email_form=None, show_email_form=None, email_me_form=None):
    data = {}

    if request.GET.get('notification_id', None) == 'success':
        data['account_notification'] = 'Settings saved.'
    else:
        data['account_notification'] = ''

    # Store edit_email_form in data[], even if we weren't passed one
    if edit_email_form is None:
        edit_email_form = mysite.account.forms.EditEmailForm(
            instance=request.user, prefix='edit_email')
    data['edit_email_form'] = edit_email_form

    if show_email_form is None:
        show_email = request.user.get_profile().show_email
        prefix = "show_email"
        data['show_email_form'] =  mysite.account.forms.ShowEmailForm(
                initial={'show_email': show_email}, prefix=prefix)
    else:
        data['show_email_form'] = show_email_form

    if email_me_form is None:
        email_me_form = mysite.account.forms.EmailMeForm(
            instance=request.user.get_profile(), prefix='email_me')
    data['email_me_form'] = email_me_form

    return (request, 'account/edit_contact_info.html', data)

@login_required
def edit_contact_info_do(request):
    # Handle "Edit email"
    edit_email_form = mysite.account.forms.EditEmailForm(
            request.POST, prefix='edit_email', instance=request.user)

    show_email_form = mysite.account.forms.ShowEmailForm(
            request.POST, prefix='show_email')

    email_me_form = mysite.account.forms.EmailMeForm(
            request.POST, prefix='email_me', instance=request.user.get_profile())

    # Email saving functionality requires two forms to both be
    # valid. This really ought to be the same form, anyway.
    if (edit_email_form.is_valid() and show_email_form.is_valid()):

        # Note that we don't need to check the validity of the EmailMeForm,
        # because it contains only an optional BooleanField.
        p = email_me_form.save()
        p.show_email = show_email_form.cleaned_data['show_email']
        p.save()

        logging.debug('Changing email of user <%s> to <%s>' % (
                request.user, edit_email_form.cleaned_data['email']))
        edit_email_form.save()

        return HttpResponseRedirect(reverse(edit_contact_info) +
                                    '?notification_id=success')
    else:
        return edit_contact_info(request,
                edit_email_form=edit_email_form,
                show_email_form=show_email_form)

@login_required
@view
def change_password(request, change_password_form = None):
    # {{{

    if change_password_form is None:
        change_password_form = django.contrib.auth.forms.PasswordChangeForm({})

    change_password_form.fields['old_password'].label = "Current password"
    change_password_form.fields['new_password2'].label = "Type it again"

    if request.GET.get('notification_id', None) == 'success':
        account_notification = 'Your password has been changed.'
    else:
        account_notification = ''

    return (request, 'account/change_password.html',
            {'change_password_form': change_password_form,
             'account_notification': account_notification})
    # }}}

@login_required
@view
def edit_fields(request, edit_fields_form = None, edit_displayed_fields_cards_form = None,
                edit_displayed_fields_list_form = None, edit_view_type_form=None,
                edit_exported_fields_form = None):
    if not _has_group(request.user, 'ADMIN') and not _has_group(request.user, 'PROJECT_PARTNER'):
        return (request, 'account/settings.html', {})

    if edit_fields_form is None:
        edit_fields_form = EditFieldsForm()
    if edit_displayed_fields_cards_form is None:
        edit_displayed_fields_cards_form = EditFieldsDisplayedInSearchForm(user=request.user, type=u'cards')
    if edit_displayed_fields_list_form is None:
        edit_displayed_fields_list_form = EditFieldsDisplayedInSearchForm(user=request.user, type=u'list')
    if edit_exported_fields_form is None:
        edit_exported_fields_form = EditExportedFieldsForm(user=request.user)
    if edit_view_type_form is None:
        edit_view_type_form = EditViewTypeForm(initial={"view_list": request.user.get_profile().view_list})

    return (request, 'account/edit_fields.html', {'edit_fields_form': edit_fields_form,
                                                  'edit_displayed_fields_cards_form': edit_displayed_fields_cards_form,
                                                  'edit_displayed_fields_list_form': edit_displayed_fields_list_form,
                                                  'edit_view_type_form': edit_view_type_form,
                                                  'edit_exported_fields_form': edit_exported_fields_form })

@login_required
def edit_fields_do(request):
    edit_fields_form = mysite.account.forms.EditFieldsForm(request.POST)
    if edit_fields_form.is_valid():
        for question in edit_fields_form.questions:
            FormQuestion.objects.filter(pk__exact=question.id).update(display_name=edit_fields_form[
                'question_%s' % question.id].value())

        return HttpResponseRedirect(reverse(edit_fields) + '?notification_id=success')
    else:
        return edit_fields(request, edit_fields_form=edit_fields_form)

@login_required
def edit_view_type_do(request):
    edit_view_type_form = mysite.account.forms.EditViewTypeForm(request.POST)
    person = request.user.get_profile()
    if edit_view_type_form.is_valid():
        person.view_list = str2bool(edit_view_type_form['view_list'].data)
        person.save()
        return HttpResponseRedirect(reverse(edit_fields) + '?notification_id=success')
    else:
        return edit_fields(request, edit_view_type_form=edit_view_type_form)

@login_required
def edit_displayed_fields_cards_do(request):
    edit_displayed_fields_cards_form = mysite.account.forms.EditFieldsDisplayedInSearchForm(request.POST,
                                                                                            user=request.user,
                                                                                            type=u'cards')
    if edit_displayed_fields_cards_form.is_valid():
        questions = FormQuestion.objects.all()
        person = Person.objects.get(user__pk__exact=request.user.id)
        CardDisplayedQuestion.objects.filter(person__user__pk__exact=request.user.id).delete()
        if edit_displayed_fields_cards_form['questions_cards'].value():
            for id in edit_displayed_fields_cards_form['questions_cards'].value():
                field = CardDisplayedQuestion(question=questions.get(pk__exact=id), person=person)
                field.save()

        return HttpResponseRedirect(reverse(edit_fields) + '?notification_id=success')
    else:
        return edit_fields(request, edit_displayed_fields_cards_form=edit_displayed_fields_cards_form)

@login_required
def edit_displayed_fields_list_do(request):
    edit_displayed_fields_list_form = mysite.account.forms.EditFieldsDisplayedInSearchForm(request.POST,
                                                                                           user=request.user,
                                                                                           type=u'list')
    if edit_displayed_fields_list_form.is_valid():
        questions = FormQuestion.objects.all()
        person = Person.objects.get(user__pk__exact=request.user.id)
        ListDisplayedQuestion.objects.filter(person__user__pk__exact=request.user.id).delete()
        if edit_displayed_fields_list_form['questions_list'].value():
            for id in edit_displayed_fields_list_form['questions_list'].value():
                field = ListDisplayedQuestion(question=questions.get(pk__exact=id), person=person)
                field.save()

        return HttpResponseRedirect(reverse(edit_fields) + '?notification_id=success')
    else:
        return edit_fields(request, edit_displayed_fields_list_form=edit_displayed_fields_list_form)

@login_required
def edit_exported_fields_do(request):
    edit_exported_fields_form = EditExportedFieldsForm(request.POST, user=request.user)

    if edit_exported_fields_form.is_valid():
        questions = FormQuestion.objects.all()
        person = Person.objects.get(user__pk__exact=request.user.id)
        ExportQuestion.objects.filter(person__user__pk__exact=request.user.id).delete()
        if edit_exported_fields_form['exported_fields'].value():
            for id in edit_exported_fields_form['exported_fields'].value():
                field = ExportQuestion(question=questions.get(pk__exact=id), person=person)
                field.save()

        return HttpResponseRedirect(reverse(edit_fields) + '?notification_id=success')
    else:
        return edit_fields(request, edit_exported_fields_form=edit_exported_fields_form)

@login_required
@view
def edit_name(request, edit_name_form = None):
    # {{{

    if edit_name_form is None:
        edit_name_form = mysite.account.forms.EditNameForm(instance=request.user)

    if request.GET.get('notification_id', None) == 'success':
        if request.user.first_name or request.user.last_name:
            account_notification = 'You have a new name.'
        else:
            account_notification = """You've removed your full name.
            We'll identify you by your username."""
    else:
        account_notification = ''

    return (request, 'account/edit_name.html',
            {'edit_name_form': edit_name_form,
             'account_notification': account_notification})
    # }}}

@login_required
def edit_name_do(request):
    user = request.user
    edit_name_form = mysite.account.forms.EditNameForm(
        request.POST, instance=user)
    if edit_name_form.is_valid():
        edit_name_form.save()

        return HttpResponseRedirect(reverse(edit_name) +
                                    '?notification_id=success')
    else:
        return edit_name(request,
                edit_name_form=edit_name_form)

@login_required
@view
def set_location(request, edit_location_form = None):
    # {{{

    person = None
    user_id = None
    if 'person_id' in request.GET and _has_group(request.user, 'ADMIN'):
        person = Person.objects.get(pk__exact=request.GET.get('person_id'))
    else:
        person = request.user.get_profile()

    data = {}
    initial = {}
    data['person_id'] = person.id

    # If the user's location is the default one, then we create a guess.
    if (not person.location_display_name) or (person.location_display_name == mysite.profile.models.DEFAULT_LOCATION):
        geoip_guess = mysite.profile.view_helpers.get_geoip_guess_for_ip(
            mysite.base.middleware.get_user_ip(request))[1]
        initial['location_display_name'] = geoip_guess
    else:
        initial['location_display_name'] = person.location_display_name

    # Initialize edit location form
    if edit_location_form is None:
        edit_location_form = mysite.account.forms.EditLocationForm(
                prefix='edit_location', instance=person, initial=initial)

    data['edit_location_form'] = edit_location_form

    if request.GET.get('notification_id', None) == 'success':
        data['account_notification'] = 'Saved.'
    else:
        data['account_notification'] = ''

    return (request, 'account/set_location.html', data)
    # }}}

@login_required
def set_location_do(request):
    if 'person_id' in request.POST and len(request.POST.get('person_id')) > 0\
        and _has_group(request.user, 'ADMIN'):
        user_profile = Person.objects.get(pk__exact=request.POST.get('person_id'))
    else:
        user_profile = request.user.get_profile()
    edit_location_form = mysite.account.forms.EditLocationForm(
        request.POST,
        instance=user_profile, prefix='edit_location')
    if edit_location_form.is_valid():
        address = edit_location_form.cleaned_data['location_display_name']
        as_string = mysite.base.view_helpers.cached_geocoding_in_json(address)
        as_dict = json.loads(as_string)
        if 'latitude' and 'longitude' in as_dict:
            user_profile.latitude = as_dict['latitude']
            user_profile.longitude = as_dict['longitude']
        else:
            user_profile.location_display_name = mysite.profile.models.DEFAULT_LOCATION
            user_profile.latitude = mysite.profile.models.DEFAULT_LATITUDE
            user_profile.longitude = mysite.profile.models.DEFAULT_LONGITUDE
        user_profile.location_confirmed = True
        user_profile.save()
        edit_location_form.save()

        return HttpResponseRedirect(reverse(set_location) +
                                    '?notification_id=success&person_id=%s' % user_profile.id)
    else:
        return set_location(request,
                edit_location_form=edit_location_form)

@login_required
def confirm_location_suggestion_do(request):
    person = request.user.get_profile()
    person.location_confirmed = True
    person.save()
    return HttpResponse()

@login_required
def dont_guess_location_do(request):
    person = request.user.get_profile()
    person.dont_guess_my_location = True
    person.location_display_name = ''
    person.save()
    return HttpResponse()

@login_required
def change_password_do(request):
    # {{{
    form = django.contrib.auth.forms.PasswordChangeForm(
            request.user, request.POST)
    if form.is_valid():
        form.save()
        clear_user_sessions(request.user, session_to_omit=request.session)
        return HttpResponseRedirect(
            reverse(change_password) + '?notification_id=success')
    else:
        return change_password(request, change_password_form=form)
    # }}}

@login_required
@view
def widget(request):
    data = {}
    data.update(mysite.base.view_helpers.get_uri_metadata_for_generating_absolute_links(
        request))
    return (request, 'account/widget.html', data)

@login_required
@view
def invite_someone(request):
    return (request, 'account/invite_someone.html', {})

def proxyconnect_sso(request):
    '''This function implements the ProxyConnect single
    sign-on API described by Vanilla Forums.

    More documentation: http://vanillaforums.org/page/singlesignon
    '''
    if request.user.is_authenticated():
        return mysite.base.decorators.as_view(
            request, 'vanilla-proxy-connect-sso.txt', {}, 'proxyconnect-sso')
    # Vanilla wants a 0-byte response if you are not logged in.
    return HttpResponse("")

@login_required
def invite_someone_do(request):
    remaining_invitations = InvitationKey.objects.remaining_invitations_for_user(
        request.user)

    form = InvitationKeyForm(data=request.POST)
    if form.is_valid():
        if remaining_invitations > 0:
            invitation = InvitationKey.objects.create_invitation(request.user)
            invitation.send_to(form.cleaned_data["email"])
            # Yay! Redirect back to invite page, with message saying who
            # was just invited.
            return HttpResponseRedirect(
                reverse(invite_someone) + '?invited=' +
                urllib.quote(form.cleaned_data['email']))
        else: # yes, there's an email; no, the guy can't invite
            return invite_someone(request, form=form,
                                  error_message='No more invites.')
    else:
        return invite_someone(request, form=form)

### The following is copied here from django_authopenid, and then
### modified trivially in the POST handler.
@django_authopenid.views.not_authenticated
def register(request, template_name='authopenid/complete.html',
             redirect_field_name=django.contrib.auth.REDIRECT_FIELD_NAME,
             register_form=django_authopenid.forms.OpenidRegisterForm,
             auth_form=django.contrib.auth.forms.AuthenticationForm,
             register_account=django_authopenid.views.register_account, send_email=False,
             extra_context=None):
    """
    register an openid.

    If user is already a member he can associate its openid with
    its account.

    A new account could also be created and automaticaly associated
    to the openid.

    :attr request: request object
    :attr template_name: string, name of template to use,
    'authopenid/complete.html' by default
    :attr redirect_field_name: string, field name used for redirect. by default
    'next'
    :attr register_form: form use to create a new account. By default
    `OpenidRegisterForm`
    :attr auth_form: form object used for legacy authentification.
    by default `OpenidVerifyForm` form auser auth contrib.
    :attr register_account: callback used to create a new account from openid.
    It take the register_form as param.
    :attr send_email: boolean, by default True. If True, an email will be sent
    to the user.
    :attr extra_context: A dictionary of variables to add to the template
    context. Any callable object in this dictionary will be called to produce
    the end result which appears in the context.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    openid_ = request.session.get('openid', None)
    if openid_ is None or not openid_:
        return HttpResponseRedirect("%s?%s" % (reverse('user_signin'),
                                urllib.urlencode({
                                redirect_field_name: redirect_to })))

    nickname = ''
    email = ''
    if openid_.sreg is not None:
        nickname = openid_.sreg.get('nickname', '')
        email = openid_.sreg.get('email', '')
    if openid_.ax is not None and not nickname or not email:
        if openid_.ax.get('http://schema.openid.net/namePerson/friendly', False):
            nickname = openid_.ax.get('http://schema.openid.net/namePerson/friendly')[0]
        if openid_.ax.get('http://schema.openid.net/contact/email', False):
            email = openid_.ax.get('http://schema.openid.net/contact/email')[0]


    form1 = register_form(initial={
        'username': nickname,
        'email': email,
    })
    form2 = auth_form(initial={
        'username': nickname,
    })

    if request.POST:
        user_ = None
        if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        if 'email' in request.POST.keys():
            form1 = register_form(data=request.POST)
            if form1.is_valid():
                user_ = register_account(form1, openid_)

                extra_profile_form = mysite.account.forms.SignUpIfYouWantToHelpForm(
                    request.POST, prefix='extra_profile_form')
                if extra_profile_form.is_valid():
                    person = user_.get_profile()
                    method2contact_info = {
                        'forwarder': 'You can reach me by email at $fwd',
                        'public_email': 'You can reach me by email at %s' % user_.email,
                        }
                    info = method2contact_info[extra_profile_form.cleaned_data[
                        'how_should_people_contact_you']]
                    person.contact_blurb = info
                    person.save()

        else:
            form2 = auth_form(data=request.POST)
            if form2.is_valid():
                user_ = form2.get_user()
        if user_ is not None:
            # associate the user to openid
            uassoc = django_authopenid.models.UserAssociation(
                        openid_url=str(openid_),
                        user_id=user_.id
            )
            uassoc.save(send_email=send_email)
            django.contrib.auth.login(request, user_)
            return HttpResponseRedirect(redirect_to)

    return render_response(request, template_name, {
        'form1': form1,
        'form2': form2,
        'extra_profile_form': mysite.account.forms.SignUpIfYouWantToHelpForm(
            prefix='extra_profile_form'),
        redirect_field_name: redirect_to,
        'nickname': nickname,
        'email': email
    }, context_instance=django_authopenid.views._build_context(request, extra_context=extra_context))

def insert_volunteer(request):
    form = mysite.account.forms.InsertVolunteerForm(request.POST)
    first_name = form['first_name'].data
    last_name = form['last_name'].data
    email = form['email'].data
    username = email
    password = "super-secret"
    user = User.objects.create(username = username, first_name = first_name, last_name = last_name, email = email, password = password)
    user.save()
    person = Person.objects.get(user=user)
    for skill in form['skills'].data:
        person.skill.add(Skill.objects.get(name=skill))
    for language in form['languages'].data:
        person.language.add(Language.objects.get(name=language))
    for cause in form['causes_you_want_to_contribute_to'].data:
        person.cause.add(Cause.objects.get(name=cause))
    for org in form['hfoss_organizations_that_interest_you'].data:
        person.organization.add(Organization.objects.get(name=org))
    person.company_name = form['company_event_organization'].data
    person.comment = form['comments'].data
    person.linked_in_url = form['linkedin_profile_url'].data
    person.language_spoken = form['what_languages'].data
    person.github_name = form['github_profile___username'].data
    person.other_name = form['other'].data
    person.google_code_name = form['google_code'].data
    time_to_commit = form['how_much_time_would_you_like_to_commit_to_volunteering'].data
    if time_to_commit:
        person.time_to_commit = TimeToCommit.objects.get(name=time_to_commit)
    heard_from = Heard_From.objects.filter(name=form['how_did_you_hear_about_socialcoding4good'].data)
    if len(heard_from) > 0:
        person.heard_from = heard_from[0]
    person.subscribed = form['yes'].data == "yes"
    person.language_spoken = form['what_languages'].data
    person.comment = form['comments'].data
    experience_level = form['Experience_level'].data
    if experience_level:
        person.experience = Experience.objects.get(name=experience_level)
    person.save()
    return django.shortcuts.redirect("http://www.socialcoding4good.org/volunteering/volunteer")

### We use this "not_authenticated" wrapper so that if you *are* logged in, you go
### straight to the ?next= value.
login = django_authopenid.views.not_authenticated(django.contrib.auth.views.login)

# vim: ai ts=3 sts=4 et sw=4 nu
