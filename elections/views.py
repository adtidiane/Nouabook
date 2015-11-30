# encoding=utf-8
import logging
from candideitorg.forms import BackgroundAdminForm
from django.core.mail.backends import console
from django.http.request import QueryDict
from django.template import context

import simplejson as json
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, TemplateView
from elections.models import Election, VotaInteligenteMessage, VotaInteligenteAnswer, CandidatePerson, Attachment, \
    NouabookItem
from elections.forms import DeputeSearchForm, QuestionFormV2, BackgroundCandidateForm, VotaInteligenteAnswerForm, \
    StatusUpdateCreateForm, Status_QuestionForm, QuestionXFormV2, QuestionXTagFormV2
from candideitorg.models import Candidate, Background, BackgroundCandidate, PersonalDataCandidate, Link
from popit.models import Person
from taggit.models import Tag, TaggedItem
from writeit.models import Message
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from secretballot.views import vote
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from elections.forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSet, InlineFormSetView
from extra_views.generic import GenericInlineFormSet
from django.views.generic.edit import UpdateView, FormView
from django.shortcuts import render, redirect
import pytumblr
#from django.conf import settings

#this function is not used anymore
def login_page(request):
    message = None
    logged_user_name = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    logged_user = CandidatePerson.objects.get(canUsername=user.id)
                    request.session['logged_user_id'] = logged_user.id
                    # logged_user_name = logged_user.candidate
                    # return render(request, 'mp_profile.html', {'message': message, 'logged_user_name': logged_user_name})
                    return HttpResponseRedirect("/profil_account/{0}".format(logged_user.candidate.slug))
                else:
                    message = "username inactif"
            else:
                message = "incorrect user or password"
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', locals())


logger = logging.getLogger(__name__)

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class CitizeTimelineView(TemplateView):
    model = NouabookItem

    def get_context_data(self, **kwargs):
        context = super(CitizeTimelineView, self).get_context_data(**kwargs)
        context['attachments'] = Attachment.objects.filter(modelName='status_update')
        context['status_updates'] = NouabookItem.objects.order_by('-created')

        return context


class AnswerWebHook(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(AnswerWebHook, self).dispatch(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        person_id = self.request.POST.get('person_id')
        content = self.request.POST.get('content')

        message_id = self.request.POST.get('message_id')
        try:
            message = VotaInteligenteMessage.objects.get(url=message_id)
            person = Person.objects.get(popit_url=person_id)
            VotaInteligenteAnswer.objects.create(person=person, message=message, content=content)
        except Exception, e:
            logger.error(e)

        response = HttpResponse(content_type="text/plain", status=200)
        return response


def vote_ajax(request):
    html_return = ''
    if 'value' in request.GET and 'type' in request.GET and request.GET['type'] == 'question':
        try:
            message = VotaInteligenteMessage.objects.get(message_ptr_id=request.GET['value'])
            return vote(request, VotaInteligenteMessage, request.GET['value'], 1)
        except ObjectDoesNotExist:
            return HttpResponse('veuillez votez correctement')
    elif 'value' in request.GET and 'type' in request.GET and request.GET['type'] == 'reponse':
        try:
            message = VotaInteligenteAnswer.objects.get(id=request.GET['value'])
            return vote(request, VotaInteligenteAnswer, request.GET['value'], 1)
        except ObjectDoesNotExist:
            return HttpResponse('veuillez votez correctement')
    else:
        return HttpResponse('veuillez votez correctement')

# GEt depute research
from django.utils.text import normalize_newlines
from django.utils.safestring import mark_safe


def the_candidatesv2(request):
    lelection = Election.objects.get(name='Marruecos2014')
    list_candidat = []
    lg = translation.get_language()
    the_candidates = lelection.can_election.candidate_set.all()
    if lg == 'fr':
        bc = Background.objects.filter(pk__in=[1, 2, 6])
        for OneCandidate in the_candidates:
            back_dict = []
            extras = OneCandidate.backgroundcandidate_set.filter(background__in=bc).order_by('background__id')
            result = ""
            for extra in extras:
                result += normalize_newlines(extra.value).replace('\n', ' ') + u" "
                back_dict.append(extra.value)
            candidat_dict = {'label': OneCandidate.name + u" " + mark_safe(result), 'ville': back_dict[1],
                             'parti': back_dict[0], 'commission': back_dict[2],
                             'name': OneCandidate.name, 'value': OneCandidate.slug}
            list_candidat.append(candidat_dict)
    else:
        bc = Background.objects.filter(pk__in=[10, 11, 15, 19])
        for OneCandidate in the_candidates:
            back_dict = []
            extras = OneCandidate.backgroundcandidate_set.filter(background__in=bc).order_by('background__id')
            result = ""
            for extra in extras:
                result += normalize_newlines(extra.value).replace('\n', ' ') + u" "
                back_dict.append(extra.value)
            candidat_dict = {'label': back_dict[3] + u" " + mark_safe(result), 'ville': back_dict[1],
                             'parti': back_dict[0], 'commission': back_dict[2],
                             'name': back_dict[3], 'value': OneCandidate.slug}
            list_candidat.append(candidat_dict)
    return HttpResponse(json.dumps(list_candidat), mimetype="application/json")


def the_candidates(request):
    lelection = Election.objects.get(name='Marruecos2014')
    the_candidates = lelection.can_election.candidate_set.all()
    bc = Background.objects.filter(name__in=['Parti politique', 'Commission', 'Circonscription'])
    list_candidat = []
    for OneCandidate in the_candidates:
        back_dict = []
        extras = OneCandidate.backgroundcandidate_set.filter(background__in=bc).order_by('background__name')
        result = ""
        for extra in extras:
            result += normalize_newlines(extra.value).replace('\n', ' ') + u" "
            back_dict.append(extra.value)
        candidat_dict = {'label': OneCandidate.name + u" " + mark_safe(result), 'ville': back_dict[0],
                         'parti': back_dict[2], 'commission': back_dict[1],
                         'name': OneCandidate.name, 'value': OneCandidate.slug}
        list_candidat.append(candidat_dict)
    return HttpResponse(json.dumps(list_candidat), mimetype="application/json")


# home pour new template	v2
class Home3View(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(Home3View, self).get_context_data(**kwargs)
        context['election'] = Election.objects.get(slug="marruecos2014")
        context['answerAttachments'] = Attachment.objects.filter(modelName='answer')
        context['status_updates'] = NouabookItem.objects.order_by('-created')[:6]
        context['writeitmessages'] = VotaInteligenteMessage.objects.filter(
            writeitinstance=context['election'].writeitinstance, moderated=True,
            answers__isnull=False).prefetch_related('answers').order_by('-answers__created')[:3]
        context['questions'] = VotaInteligenteMessage.objects.filter(
            writeitinstance=context['election'].writeitinstance, answers__isnull=True, moderated=True).order_by(
            '-moderated_at')[:5]
        context['top_vote'] = VotaInteligenteMessage.objects.filter(writeitinstance=context['election'].writeitinstance,
                                                                    answers__isnull=True, moderated=True).order_by(
            '-total_upvotes')[:5]
        lg = translation.get_language()
        if lg == 'fr':
            context['backgrounds'] = Background.objects.filter(pk__in=[1, 2, 6])
        else:
            context['backgrounds'] = Background.objects.filter(pk__in=[10, 11, 15, 19]).order_by('id')
        context['canreachable'] = context['election'].can_election.candidate_set.filter(
            relation__reachable=True).order_by('name')
        return context


# depute v1
class ElectionDeputeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ElectionDeputeView, self).get_context_data(**kwargs)
        marueccos = Election.objects.get(slug="marruecos2014")
        context['deputes'] = marueccos.can_election.candidate_set.all().order_by('photo')
        context['slug_election'] = 'marruecos2014'
        context['background'] = Background.objects.filter(
            Q(name__icontains="Parti politique") | Q(name="Circonscription")).order_by('-name')
        return context


# profil
class ProfilDetailView(DetailView):
    model = Candidate

    def get_queryset(self):
        queryset = super(ProfilDetailView, self).get_queryset()
        queryset = queryset.filter(election__slug="marruecos2014")  # self.kwargs['election_slug']

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProfilDetailView, self).get_context_data(**kwargs)
        # I know this is weird but this is basically
        # me the candidate.candideitorg_election.votainteligente_election
        # so that's why it says election.election
        l_election = self.object.election.election
        context['mp_tags'] = self.object.relation.tags.all()
        #context['mp_tags'] = TaggedItem.objects.values_list('tag_id', flat=True).filter(object_id = self.object.relation.person.id, content_type_id = 33)
        context['attachments'] = Attachment.objects.filter(modelName='status_update', author_id=self.object.relation.person.id)
        context['answerAttachments'] = Attachment.objects.filter(modelName='answer', author_id=self.object.relation.person.id)
        context['status_updates'] = NouabookItem.objects.filter(candidate__slug=self.kwargs['slug'])
        context['writeitmessages'] = VotaInteligenteMessage.objects.filter(people=self.object.relation.person,
                                                                           moderated=True).prefetch_related(
            'answers').order_by('-moderated_at')
        lg = translation.get_language()

        le_parti = BackgroundCandidate.objects.get(background_id= 1, candidate_id= self.object.relation.person.id).value
        context['banniere'] = le_parti[le_parti.find('(')+1:len(le_parti)-1].lower()
        if lg == 'fr':
            context['background_categories'] = l_election.can_election.backgroundcategory_set.filter(
                Q(name__icontains="Information") | Q(name__icontains="Affiliation")).order_by('-name')
            context['personal_datas'] = l_election.can_election.personaldata_set.all()
        else:
            context['background_categories'] = l_election.can_election.backgroundcategory_set.filter(
                id__in=[3, 4]).order_by('id')
            context['personal_data_ar'] = Background.objects.filter(background_category_id=5).order_by('id')
        return context


class ItemInline(InlineFormSet):
    model = BackgroundCandidate
    #form_class = BackgroundCandidateForm
    fields = ['value']


class PersonalInline(InlineFormSet):
    model = PersonalDataCandidate
    fields = ['value']

class LinkInline(InlineFormSet):
    model = Link
    fields = ['url']

class TagInline(InlineFormSetView):
    model = Tag
    #form_class = BackgroundCandidateForm
    def get_object(self):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        return Tag.objects.filter(object_id=logged_user.candidate.id)


# profil Account
class ProfilAccountDetailView(LoginRequiredMixin, UpdateWithInlinesView):
    model = Candidate
    template_name = "elections/account/mp_profile.html"
    fields = ('name',)
    inlines = [ItemInline, PersonalInline, LinkInline]

    def get_object(self):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        return logged_user.candidate

    def get_context_data(self, **kwargs):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        context = super(ProfilAccountDetailView, self).get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['mp_tags'] = TaggedItem.objects.values_list('tag_id', flat=True).filter(object_id = self.object.relation.person.id, content_type_id = 33)
        context['les_partis'] = BackgroundCandidate.objects.values_list('value', flat=True).filter(background_id=1).order_by('value').distinct()
        context['les_partis_ar'] = BackgroundCandidate.objects.values_list('value', flat=True).filter(background_id=10).order_by('value').distinct()
        context["changer_photo"] = _(u"Changement de photo député")

        return  context

    # def form_invalid(self, **kwargs):
    #     return self.render_to_response(self.get_context_data(**kwargs))

class UpdateOrderView(UpdateWithInlinesView):
    model = Candidate
    fields = ('name',)
    template_name = "elections/account/mp_profile_update.html"
    inlines = [ItemInline]

    def get_object(self):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        return logged_user.candidate

    def get_success_url(self):
        return self.object.get_absolute_url()


# profil_account_questions
class ProfileQuestionView(LoginRequiredMixin, DetailView):
    model = Candidate

    def get_object(self):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        return logged_user.candidate

    def get_queryset(self):
        queryset = super(ProfileQuestionView, self).get_queryset()
        queryset = queryset.filter(election__slug="marruecos2014")  # self.kwargs['election_slug']

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProfileQuestionView, self).get_context_data(**kwargs)
        # I know this is weird but this is basically
        # me the candidate.candideitorg_election.votainteligente_election
        # so that's why it says election.election
        l_election = self.object.election.election
        context['writeitmessages'] = VotaInteligenteMessage.objects.filter(people=self.object.relation.person,
                                                                           moderated=True).prefetch_related(
            'answers').order_by('-moderated_at')
        lg = translation.get_language()
        context['AnswerAttachments'] = Attachment.objects.filter(modelName='answer', author_id=self.object.relation.person.id)
        if self.kwargs['success'] is not None and self.kwargs['success'] == 'succes':
            context['message_done'] = self.kwargs['success']
        return context


# question v2
class ElectionQuestionView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ElectionQuestionView, self).get_context_data(**kwargs)
        context['election'] = Election.objects.get(slug="marruecos2014")
        context['tags'] = Tag.objects.all()
        context['attachments'] = Attachment.objects.filter(modelName='answer')
        context['writeitmessages'] = VotaInteligenteMessage.objects.filter(
            writeitinstance=context['election'].writeitinstance, moderated=True,
            answers__isnull=False).prefetch_related('answers').order_by('-answers__created')
        if self.kwargs['success'] is not None and self.kwargs['success'] == 'succes':
            context['message_done'] = self.kwargs['success']
        return context


# Posez
class ElectionPosezView(CreateView):
    model = Message
    form_class = QuestionFormV2
    # initial = {'people': '2'}

    def get_context_data(self, **kwargs):
        context = super(ElectionPosezView, self).get_context_data(**kwargs)
        # self.initial = {'people': self.kwargs['pk']}
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ElectionPosezView, self).get_form_kwargs()
        election = Election.objects.get(slug="marruecos2014")
        kwargs['election'] = election
        # kwargs['initial']={'people':'2'}
        return kwargs

    def get_success_url(self):
        return reverse('question_view', kwargs={'success': 'succes', })

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# Posez X
class ElectionPosezXView(CreateView):
    model = Message
    form_class = QuestionXFormV2
    # initial = {'people': '2'}

    def get(self, request, *args, **kwargs):
        try:
            c = CandidatePerson.objects.get(id=self.kwargs['pk'], reachable=True)
            return super(ElectionPosezXView, self).get(request, *args, **kwargs)
        except:
            return redirect('posez_view')

    def get_context_data(self, **kwargs):
        context = super(ElectionPosezXView, self).get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.get(id=self.kwargs['pk'])
        context['redirection'] = '/posez/'+self.kwargs['pk']
        # self.initial = {'people': self.kwargs['pk']}
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ElectionPosezXView, self).get_form_kwargs()
        election = Election.objects.get(slug="marruecos2014")
        kwargs['election'] = election
        kwargs['candidateId'] = self.kwargs['pk']
        # kwargs['initial']={'people':'2'}
        return kwargs

    def get_success_url(self):
        return reverse('question_view', kwargs={'success': 'succes', })

    def get_initial(self, **kwargs):
        par_defaut = {}
        if self.kwargs['pk'] is not None:
            the_pk = self.kwargs['pk']
            par_defaut = {'people': [the_pk, ], }
        return par_defaut

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

# Posez X on Tag
class ElectionPosezXTagView(CreateView):
    model = Message
    form_class = QuestionXTagFormV2
    # initial = {'people': '2'}

    def get(self, request, *args, **kwargs):
        try:
            c = CandidatePerson.objects.get(id=self.kwargs['pk'], reachable=True)
            tag = c.tags.get(id=self.kwargs['tag'])
            return super(ElectionPosezXTagView, self).get(request, *args, **kwargs)
        except:
            return redirect('posez_view')

    """def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return HttpResponse('test post') #form.cleaned_data['people']

    def form_valid(self, form):
        return HttpResponse('test form_valid')"""

    def get_context_data(self, **kwargs):
        context = super(ElectionPosezXTagView, self).get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.get(id=self.kwargs['pk'])
        context['redirection'] = '/posez/'+self.kwargs['pk']+'-theme-'+self.kwargs['tag']
        # self.initial = {'people': self.kwargs['pk']}
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ElectionPosezXTagView, self).get_form_kwargs()
        election = Election.objects.get(slug="marruecos2014")
        kwargs['election'] = election
        kwargs['candidateId'] = self.kwargs['pk']
        # kwargs['initial']={'people':'2'}
        return kwargs

    def get_success_url(self):
        return reverse('question_view', kwargs={'success': 'succes', })

    def get_initial(self, **kwargs):
        par_defaut = {}
        if self.kwargs['pk'] is not None:
            the_pk = self.kwargs['pk']
            the_tag = self.kwargs['tag']
            par_defaut = {'people': [the_pk, ], 'tags': [the_tag, ], }
        return par_defaut

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AnswerQuestionFormView(LoginRequiredMixin, CreateView):
    model = VotaInteligenteAnswer

    form_class = VotaInteligenteAnswerForm

    # success_url = 'profile/questions/'

    def get_context_data(self, **kwargs):
        context = super(AnswerQuestionFormView, self).get_context_data(**kwargs)
        context['message_to_answer'] = VotaInteligenteMessage.objects.get(pk=self.kwargs['pk'])
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        context['candidate'] = Candidate.objects.get(pk=logged_user.candidate.id)
        # self.initial = {'people': self.kwargs['pk']}
        context['redirection'] = '/accounts/profile/questions/message-' + self.kwargs['pk']
        return context

    '''def get_form_kwargs(self, **kwargs):
        kwargs = super(AnswerQuestionFormView, self).get_form_kwargs()
        election = Election.objects.get(slug="marruecos2014")
        kwargs['election'] = election
        # kwargs['initial']={'people':'2'}
        return kwargs'''

    def get_success_url(self):
        return reverse('account_question_view', kwargs={'success': 'succes', })

    def get_initial(self, **kwargs):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        par_defaut = {'person': logged_user.candidate.id, 'message': self.kwargs['pk']}
        '''if self.kwargs['pk'] is not None:
            the_pk = self.kwargs['pk']
            par_defaut = {'people': [the_pk, ], }'''
        return par_defaut

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class AnswerQuestionFormViewUpdate(LoginRequiredMixin, UpdateView):
    model = VotaInteligenteAnswer

    form_class = VotaInteligenteAnswerForm

    # success_url = 'profile/questions/'

    def get_object(self):
        answer = VotaInteligenteAnswer.objects.get(message_id=self.kwargs['pk'])
        return answer

    def get_context_data(self, **kwargs):
        context = super(AnswerQuestionFormViewUpdate, self).get_context_data(**kwargs)
        context['message_to_answer'] = VotaInteligenteMessage.objects.get(pk=self.kwargs['pk'])
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        context['candidate'] = Candidate.objects.get(pk=logged_user.candidate.id)
        context['attachments'] = Attachment.objects.filter(messageId=self.kwargs['pk'])
        # self.initial = {'people': self.kwargs['pk']}
        context['redirection'] = '/accounts/profile/questions/update/message-' + self.kwargs['pk']
        return context

    '''def get_form_kwargs(self, **kwargs):
        kwargs = super(AnswerQuestionFormView, self).get_form_kwargs()
        election = Election.objects.get(slug="marruecos2014")
        kwargs['election'] = election
        # kwargs['initial']={'people':'2'}
        return kwargs'''

    def get_success_url(self):
        return reverse('account_question_view', kwargs={'success': 'succes', })

    def get_initial(self, **kwargs):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        answer = VotaInteligenteAnswer.objects.get(message_id=self.kwargs['pk']).content
        par_defaut = {'person': logged_user.candidate.id, 'content': answer, 'message': self.kwargs['pk']}
        '''if self.kwargs['pk'] is not None:
            the_pk = self.kwargs['pk']
            par_defaut = {'people': [the_pk, ], }'''
        return par_defaut

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


@csrf_exempt
def tag_to_mp(request):
    if request.method == 'POST':

        if request.POST["selected_tags"] != '555' :
            selected_tags = request.POST["selected_tags"].split(',')
        else:
            selected_tags = []

        candidate_id = int(request.POST["candidate_id"])

        if request.POST["old_tags"] != '444' :
            old_tags = request.POST["old_tags"].split(',')
            for old_tag in old_tags :
                if old_tag not in selected_tags:
                    t = TaggedItem.objects.get(tag_id = old_tag, object_id = candidate_id, content_type_id = 33)
                    t.delete()
        else:
            old_tags = []



        for tag in selected_tags :
            if tag not in old_tags :
                t = TaggedItem(tag_id = int(tag), object_id = candidate_id, content_type_id = 33)
                t.save()

        response_data = {"updated_tags" : selected_tags}
        response_data['msg'] = 'tags updated'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@login_required
def delete_attachment(request):
    if request.method == 'DELETE':

        attachment = Attachment.objects.get(pk=int(QueryDict(request.body).get('attachment_pk')))

        attachment.file.delete()
        attachment.delete()

        response_data = {}
        response_data['msg'] = 'File was deleted.'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


class StatusUpdateCreateView(LoginRequiredMixin, CreateView):
    model = NouabookItem

    form_class = StatusUpdateCreateForm

    # success_url = 'profile/questions/'

    def get_context_data(self, **kwargs):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        context = super(StatusUpdateCreateView, self).get_context_data(**kwargs)
        context['all_status_update'] = NouabookItem.objects.filter(candidate=logged_user.candidate,
                                                                   category__name='status_update').order_by('-updated')
        context['candidate'] = Candidate.objects.get(pk=logged_user.candidate.id)
        context['attachments'] = Attachment.objects.filter(modelName='status_update', author_id=logged_user.candidate.id)
        context['AnswerAttachments'] = Attachment.objects.filter(modelName='answer', author_id=logged_user.candidate.id)
        context['questions'] = VotaInteligenteMessage.objects.filter(people=logged_user.candidate.relation.person,
                                                                     moderated=True,nouabookItem_id__isnull=False).prefetch_related(
            'answers').order_by('-moderated_at')
        # self.initial = {'people': self.kwargs['pk']}
        if self.kwargs['success'] is not None and self.kwargs['success'] == 'succes':
            context['message_done'] = self.kwargs['success']
        return context

    def get_initial(self, **kwargs):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        par_defaut = {'candidate': logged_user.candidate.id, 'category': 1}
        return par_defaut

    def get_success_url(self):
        return reverse('account_status_view', kwargs={'success': 'succes',})

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class StatusUpdateUpdateView(LoginRequiredMixin, UpdateView):
    model = NouabookItem

    form_class = StatusUpdateCreateForm

    # success_url = 'profile/questions/'

    def get_object(self):
        post = NouabookItem.objects.get(id=self.kwargs['pk'])
        return post

    def get_context_data(self, **kwargs):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        context = super(StatusUpdateUpdateView, self).get_context_data(**kwargs)
        context['candidate'] = Candidate.objects.get(pk=logged_user.candidate.id)
        context['attachments'] = Attachment.objects.filter(messageId=self.kwargs['pk'], author_id=logged_user.candidate.id)
        context['redirection'] = '/accounts/status/update/post-' + self.kwargs['pk']
        return context

    def get_initial(self, **kwargs):
        logged_user = CandidatePerson.objects.get(canUsername=self.request.user.id)
        post = NouabookItem.objects.get(id=self.kwargs['pk'])
        par_defaut = {'title': post.title, 'candidate': post.candidate, 'category': post.category, 'text': post.text,
                      'url': post.url}
        '''if self.kwargs['pk'] is not None:
            the_pk = self.kwargs['pk']
            par_defaut = {'people': [the_pk, ], }'''
        return par_defaut

    def get_success_url(self):
        return reverse('account_status_view', kwargs={'success': 'succes', })

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# Posez su status
class StatusPosezView(CreateView):
    model = Message
    form_class = Status_QuestionForm
    # initial = {'people': '2'}

    def get(self, request, *args, **kwargs):
        try:
            c = CandidatePerson.objects.get(id=self.kwargs['pk'], reachable=True)
            status=NouabookItem.objects.get(id=self.kwargs['status'])
            if c.candidate.id != status.candidate.id:
                return redirect('posez_view')
            return super(StatusPosezView, self).get(request, *args, **kwargs)
        except:
            return redirect('posez_view')

    def get_context_data(self, **kwargs):
        context = super(StatusPosezView, self).get_context_data(**kwargs)
        context['status'] = NouabookItem.objects.get(id=self.kwargs['status'])
        # self.initial = {'people': self.kwargs['pk']}
        context['redirection'] = '/posez/'+self.kwargs['pk']+'-status-'+self.kwargs['status']
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(StatusPosezView, self).get_form_kwargs()
        election = Election.objects.get(slug="marruecos2014")
        kwargs['election'] = election
        # kwargs['initial']={'people':'2'}
        return kwargs

    def get_success_url(self):
        return reverse('question_view', kwargs={'success': 'succes', })

    def get_initial(self, **kwargs):
        par_defaut = {}
        if self.kwargs['pk'] is not None:
            the_pk = self.kwargs['pk']
            status_id = self.kwargs['status']
            par_defaut = {'people': [the_pk, ], 'nouabookItem': status_id}
        return par_defaut

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# Questions view sur Status
class StatusQuestionsView(DetailView):
    model = NouabookItem

    def get_queryset(self):
        
        post = NouabookItem.objects.filter(id=self.kwargs['pk'])
        #post = NouabookItem.objects.get(id=self.kwargs['pk'])
        return post

    def get_context_data(self, **kwargs):
        context = super(StatusQuestionsView, self).get_context_data(**kwargs)
        # I know this is weird but this is basically
        # me the candidate.candideitorg_election.votainteligente_election
        # so that's why it says election.election
        context['attachments'] = Attachment.objects.filter(modelName='status_update', author_id=self.object.candidate.id)
        context['answerAttachments'] = Attachment.objects.filter(modelName='answer', author_id=self.object.candidate.id)
        context['writeitmessages'] = VotaInteligenteMessage.objects.filter(nouabookItem=self.object,
                                                                           moderated=True).prefetch_related(
            'answers').order_by('-moderated_at')
        context['redirection'] = '/questions-status/' + self.kwargs['pk']
        return context

@login_required
def delete_status(request):
    if request.method == 'DELETE':

        status = NouabookItem.objects.get(pk=int(QueryDict(request.body).get('status_pk')))

        attachments = Attachment.objects.filter(messageId=int(QueryDict(request.body).get('status_pk')))

        for each in attachments:
            each.file.delete()
            each.delete()

        status.delete()

        response_data = {}
        response_data['msg'] = 'File was deleted.'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


# Account answer message
# class AccountAnswerMessage(CreateView):
#     model = Attachment
#
#     def get_success_url(self):
#        return reverse('account_question_view', kwargs={'success': 'succes', })

# MessageView
class MessageView(DetailView):
    model = VotaInteligenteMessage

    def get_queryset(self):
        rq = VotaInteligenteMessage.objects.filter(id=self.kwargs['pk'], moderated=True)

        return rq

    def get_context_data(self, **kwargs):
        context = super(MessageView, self).get_context_data(**kwargs)
        if self.kwargs['reponse'] == '-reponse':
            context['reponse_diese'] = 'ok'
            context['redirection'] = '/questions/message-' + self.kwargs['pk'] + '-reponse'
        else:
            context['redirection'] = '/questions/message-' + self.kwargs['pk']

        context['attachments'] = Attachment.objects.filter(modelName='answer', messageId=self.kwargs['pk'])

        return context


from elections.encoder_csv import UnicodeWriter
from elections.encoder_csv import UnicodeReader


def charger_csv(request):
    response = HttpResponse(content_type='text/csv')
    response[
        'Content-Disposition'] = 'attachment; filename="newsletter.csv"'  # /home/simsim/www/votainteligente-portal-electoral/elections/templates/
    with open('/home/simsim/www/votainteligente-portal-electoral/elections/templates/newsletter.csv', 'rb') as csvfile:
        """writer = csv.writer(csvfile)
        writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
        writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])"""
        reader = UnicodeReader(csvfile)
        writer = UnicodeWriter(response)
        writer.writerows(reader)
    return response


from django.utils import translation


def welcome_translated(request):
    return HttpResponse(translation.get_language())


def deputesview(request):
    marueccos = Election.objects.get(slug="marruecos2014")
    slug_election = 'marruecos2014'
    lg = translation.get_language()
    if lg == 'fr':
        background = Background.objects.filter(pk__in=[1, 2, 6]).order_by('id')
    else:
        background = Background.objects.filter(id__in=[10, 11, 15, 19]).order_by('id')
        background_name = background[3]
    if request.method == 'GET' and 's' in request.GET and request.GET['s'] == 'search':
        form = DeputeSearchForm(request.GET)
        if form.is_valid():
            nom_mp = form.cleaned_data['nom_depute']
            parti = form.cleaned_data['parti_politique']
            circpt = form.cleaned_data['circonscription']
            pref_prov = form.cleaned_data['pref_or_prov']
            commission = form.cleaned_data['commission']
            ok = 0
            if lg == 'fr':
                bg_id_list = [1, 2, 3, 6]
            else:
                bg_id_list = [10, 11, 12, 15]
            deputes = marueccos.can_election.candidate_set
            if nom_mp:
                if lg == 'fr':
                    deputes = deputes.filter(name__icontains=nom_mp)
                else:
                    deputes = deputes.filter(backgroundcandidate__value__contains=nom_mp,
                                             backgroundcandidate__background_id=19)
                ok += 1
            if parti:
                deputes = deputes.filter(backgroundcandidate__value=parti,
                                         backgroundcandidate__background_id=bg_id_list[0])
                ok += 1
            if circpt:
                deputes = deputes.filter(backgroundcandidate__value=circpt,
                                         backgroundcandidate__background_id=bg_id_list[1])
                ok += 1
            if pref_prov:
                deputes = deputes.filter(backgroundcandidate__value=pref_prov,
                                         backgroundcandidate__background_id=bg_id_list[2])
                ok += 1
            if commission:
                deputes = deputes.filter(backgroundcandidate__value=commission,
                                         backgroundcandidate__background_id=bg_id_list[3])
                ok += 1
            if ok == 0:
                deputes = deputes.all()
            deputes = deputes.order_by('-relation__reachable', '-relation__ranking', 'name')
        else:
            msg = 'recherche invalide'
            nom_error = form.errors['nom_depute']
        return render(request, 'elections/depute_html.html', locals())
    elif request.method == 'GET' and 's' not in request.GET and 'page' in request.GET:
        deputes = marueccos.can_election.candidate_set.all().order_by('-relation__reachable', '-relation__ranking', 'name')
        return render(request, 'elections/depute_html.html', locals())
    else:
        form = DeputeSearchForm()
        # .values('value')
        deputes = marueccos.can_election.candidate_set.all().order_by('-relation__reachable', '-relation__ranking', 'name')
    return render(request, 'elections/deputes.html', locals())


# ajax for page questions
def ajax_question_view(request):
    mess_content = 'Aucune Question'
    if request.method == 'GET' and 'page' in request.GET and 'genre' in request.GET and 'tag' in request.GET:

        election = Election.objects.get(slug="marruecos2014")
        if request.GET['genre'] == '#qa':
            attachments = Attachment.objects.filter(modelName='answer')
            if request.GET['tag'] == "#" or request.GET['tag'] == "" or request.GET['tag'] == "undefined":
                the_qa = VotaInteligenteMessage.objects.filter(writeitinstance=election.writeitinstance, moderated=True,
                                                               answers__isnull=False).prefetch_related(
                    'answers').order_by('-answers__created')
            else:
                the_qa = VotaInteligenteMessage.objects.filter(writeitinstance=election.writeitinstance, moderated=True,
                                                               answers__isnull=False, tags__id=request.GET['tag']).prefetch_related(
                    'answers').order_by('-answers__created')

        elif request.GET['genre'] == '#recent':
            if request.GET['tag'] == "#" or request.GET['tag'] == "" or request.GET['tag'] == "undefined":
                recents = VotaInteligenteMessage.objects.filter(writeitinstance=election.writeitinstance,
                                                            answers__isnull=True, moderated=True).order_by('-moderated_at')
            else:
                recents = VotaInteligenteMessage.objects.filter(writeitinstance=election.writeitinstance,
                                                            answers__isnull=True, moderated=True, tags__id=request.GET['tag']).order_by('-moderated_at')
        elif request.GET['genre'] == '#popular':
            if request.GET['tag'] == "#" or request.GET['tag'] == "" or request.GET['tag'] == "undefined":
                populars = VotaInteligenteMessage.objects.filter(writeitinstance=election.writeitinstance,
                                                             answers__isnull=True, moderated=True).order_by('-total_upvotes')
            else:
                populars = VotaInteligenteMessage.objects.filter(writeitinstance=election.writeitinstance,
                                                             answers__isnull=True, moderated=True, tags__id=request.GET['tag']).order_by('-total_upvotes')
        else:
            message = mess_content
    else:
        message = mess_content
    return render(request, 'elections/question_html.html', locals())


# ajax for profil questions
def ajax_profil_question_view(request):
    mess_content = _(u'Aucun contenu')
    if request.method == 'GET' and 'page' in request.GET and 'depute' in request.GET and 'type' in request.GET and request.GET[
        'depute'].isdigit():
        try:
            candidate = Candidate.objects.get(pk=request.GET['depute'])
            if request.GET['type'] == "#qa":
                answerAttachments = Attachment.objects.filter(modelName='answer', author_id=candidate.id)
                messagesprofil = VotaInteligenteMessage.objects.filter(people=candidate.relation.person,
                                                                       moderated=True).prefetch_related('answers').order_by(
                    '-moderated_at')
            elif request.GET['type'] == "#status":
                attachments = Attachment.objects.filter(modelName='status_update', author_id=candidate.id)                
                status_updates = NouabookItem.objects.filter(candidate__id=candidate.id).order_by('-updated')
            else:
                message = mess_content
        except ObjectDoesNotExist:
            message = mess_content
    else:
        message = mess_content
    return render(request, 'elections/profil_question_status.html', locals())

# ajax for profil questions backend
def ajax_profil_question_backend(request):
    mess_content = _(u'Aucune Question')
    if request.method == 'GET' and 'page' in request.GET and 'depute' in request.GET and request.GET[
        'depute'].isdigit():
        try:
            candidate = Candidate.objects.get(pk=request.GET['depute'])
            AnswerAttachments = Attachment.objects.filter(modelName='answer', author_id=candidate.id)
            messagesprofil = VotaInteligenteMessage.objects.filter(people=candidate.relation.person,
                                                                   moderated=True).prefetch_related('answers').order_by(
                '-moderated_at')
        except ObjectDoesNotExist:
            message = mess_content
    else:
        message = mess_content
    return render(request, 'elections/account/profil_question.html', locals())


# ajax get deputes by tags
@csrf_exempt
def get_deputes_by_tag(request):
    # tag_id = QueryDict(request.body).get('tag_id')
    tag_id = request.GET['tag_id']
    data = []
    deputes = []
    lg = translation.get_language()
    if tag_id:
        deputes = CandidatePerson.objects.filter(reachable=True, tags__id=tag_id)
    else:
        data = [-1]
    if lg == 'fr':
        for depute in deputes:
            data.append({'id': depute.candidate_id, 'name': depute.candidate.name})
    else:
        for depute in deputes:
            name_arabic = BackgroundCandidate.objects.get(background_id=19, candidate=depute.candidate).value
            data.append({'id': depute.candidate_id, 'name': name_arabic})
    
    return HttpResponse(json.dumps(data), content_type="application/json")

def update_ranking(request):
    data = []
    counter = 0;
    counter2 = 0;
    chaine = 'operation success'
    # Authenticate via API Key
    """client = pytumblr.TumblrRestClient('PmuCcZRP0RXUWjxqkOmjXEdjUVHt4oyGomIQhZZTIasg9qDQBT')"""

    # Make the request
    """data = client.posts('nouabook.tumblr.com', limit=3, filter='html')
    return HttpResponse(json.dumps(data), content_type="application/json")"""
    '''for candidate in CandidatePerson.objects.filter(reachable=True):
        totalQuestionsAnswred = candidate.person.answers.count()
        if totalQuestionsAnswred < 5:
            candidate.ranking = 0
        elif totalQuestionsAnswred >= 5 and totalQuestionsAnswred < 10:
            candidate.ranking = 1
        elif totalQuestionsAnswred >= 10 and totalQuestionsAnswred < 15:
            candidate.ranking = 2
        elif totalQuestionsAnswred >= 15 and totalQuestionsAnswred < 20:
            candidate.ranking = 3
        elif totalQuestionsAnswred >= 20 and totalQuestionsAnswred < 25:
            candidate.ranking = 4
        elif totalQuestionsAnswred >= 25:
            candidate.ranking = 5

        candidate.save()
        counter += 1 '''
        

    """# add or update personaldataCandidate table for 2 new fields
    for c in Candidate.objects.all() :
        p = PersonalDataCandidate()
        p.remote_id = 12
        p.resource_uri = ''
        p.value = ''
        p.candidate_id = c.id
        p.personaldata_id = 12
        p.save()
        counter += 1

        ps = PersonalDataCandidate()
        ps.remote_id = 12
        ps.resource_uri = ''
        ps.value = ''
        ps.candidate_id = c.id
        ps.personaldata_id = 13
        ps.save()
        counter2 += 1 
     # add or update BackgroundCandidate table for 2 new fields in arabic
    for c in Candidate.objects.all() :
        p = BackgroundCandidate()
        p.remote_id = 12
        p.resource_uri = ''
        p.value = ''
        p.candidate_id = c.id
        p.background_id = 22
        p.save()
        counter += 1

        ps = BackgroundCandidate()
        ps.remote_id = 12
        ps.resource_uri = ''
        ps.value = ''
        ps.candidate_id = c.id
        ps.background_id = 23
        ps.save()
        counter2 += 1 """


    # Deputes sans lien
    """deputes_sans_lien = Candidate.objects.exclude(link__name__in = ['Twitter', 'Facebook'])

    for c in deputes_sans_lien :
        p1 = Link()
        p2 = Link()
        p3 = Link()
        p4 = Link()

        p1.remote_id = p2.remote_id = p3.remote_id = p4.remote_id = 12
        p1.resource_uri = p2.resource_uri = p3.resource_uri = p4.resource_uri = ''
        p1.name = 'Facebook'
        p2.name = 'Twitter'
        p3.name = 'Youtube'
        p4.name = 'Website'

        p1.url = p2.url = p3.url = p4.url = ''
        p1.candidate_id = p2.candidate_id = p3.candidate_id = p4.candidate_id = c.id

        p1.save()
        p2.save()
        p3.save()
        p4.save()
        counter += 1

    chaine += ' députés sans lien' """

    # Deputes avec facebook
    """deputes_aumoins_facebook = Candidate.objects.filter(link__name__in = ['Facebook'])
    deputes_facebook = deputes_aumoins_facebook.exclude(link__name__in = ['Twitter', 'Youtube', 'Website'])
    for c in deputes_facebook :
        p2 = Link()
        p3 = Link()
        p4 = Link()

        p2.remote_id = p3.remote_id = p4.remote_id = 12
        p2.resource_uri = p3.resource_uri = p4.resource_uri = ''
        p2.name = 'Twitter'
        p3.name = 'Youtube'
        p4.name = 'Website'

        p2.url = p3.url = p4.url = ''
        p2.candidate_id = p3.candidate_id = p4.candidate_id = c.id

        p2.save()
        p3.save()
        p4.save()
        counter += 1
    chaine += ' députés ayant seulement facebook'"""

    # Deputes avec twitter
    """deputes_twitter = Candidate.objects.filter(link__name__in = ['Twitter']).exclude(link__name__in = ['Facebook', 'Youtube', 'Website'])
    for c in deputes_twitter :
        p1 = Link()
        p3 = Link()
        p4 = Link()

        p1.remote_id = p3.remote_id = p4.remote_id = 12
        p1.resource_uri = p3.resource_uri = p4.resource_uri = ''
        p1.name = 'Facebook'
        p3.name = 'Youtube'
        p4.name = 'Website'

        p1.url = p3.url = p4.url = ''
        p1.candidate_id = p3.candidate_id = p4.candidate_id = c.id

        p1.save()
        p3.save()
        p4.save()
        counter += 1
    chaine += ' députés ayant seulement twitter'"""

    # Deputes avec twitter + facebook
    """deputes_twitter_facebook = Candidate.objects.filter(link__name__in = ['Twitter']).filter(link__name__in = ['Facebook'])\
        .exclude(link__name__in = ['Youtube', 'Website'])
    for c in deputes_twitter_facebook :
        p3 = Link()
        p4 = Link()

        p3.remote_id = p4.remote_id = 12
        p3.resource_uri = p4.resource_uri = ''
        p3.name = 'Youtube'
        p4.name = 'Website'

        p3.url = p4.url = ''
        p3.candidate_id = p4.candidate_id = c.id

        p3.save()
        p4.save()
        counter += 1
    chaine += ' députés ayant seulement facebook et twitter'"""

    return render(request, 'elections/ranking_update.html', locals())

def blog_ajax_view(request):
    # Authenticate via API Key
    client = pytumblr.TumblrRestClient('PmuCcZRP0RXUWjxqkOmjXEdjUVHt4oyGomIQhZZTIasg9qDQBT')

    # Make the request
    data = client.posts('nouabook.tumblr.com', limit=3, filter='html')
    return HttpResponse(json.dumps(data), content_type="application/json")