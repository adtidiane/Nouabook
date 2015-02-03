# coding=utf-8
from django.views.generic.edit import FormView
from elections.forms import ElectionSearchByTagsForm
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, TemplateView
from elections.models import Election, VotaInteligenteMessage, VotaInteligenteAnswer
from elections.forms import MessageForm, QuestionForm, NewsletterForm, DeputeSearchForm, QuestionFormV2
from candideitorg.models import Candidate, Background, BackgroundCandidate as backcan
from popit.models import Person
from writeit.models import Message
from django.views.generic.base import View
import logging
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from operator import itemgetter
from secretballot.views import vote
from django.core.exceptions import ObjectDoesNotExist
from django.utils import translation
from django.utils.translation import ugettext as _

logger = logging.getLogger(__name__)


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
            VotaInteligenteAnswer.objects.create(person =person, message=message, content=content)
        except Exception, e:
            logger.error(e)

        response = HttpResponse(content_type="text/plain", status=200)
        return response


def vote_ajax(request):
    html_return = ''
    if 'value' in request.GET and 'type' in request.GET and request.GET['type'] == 'question':
        try:
            message=VotaInteligenteMessage.objects.get(message_ptr_id=request.GET['value'])
            return vote(request, VotaInteligenteMessage, request.GET['value'], 1)
        except ObjectDoesNotExist:    
            return HttpResponse('veuillez votez correctement')
    elif 'value' in request.GET and 'type' in request.GET and request.GET['type'] == 'reponse':
        try:
            message=VotaInteligenteAnswer.objects.get(id=request.GET['value'])
            return vote(request, VotaInteligenteAnswer, request.GET['value'], 1)
        except ObjectDoesNotExist:
            return HttpResponse('veuillez votez correctement')
    else:
        return HttpResponse('veuillez votez correctement')

#GEt depute research
from django.utils.text import normalize_newlines
from django.utils.safestring import mark_safe
def the_candidatesv2(request):
    lelection = Election.objects.get(name='Marruecos2014')
    list_candidat =[]
    lg=translation.get_language()
    the_candidates = lelection.can_election.candidate_set.all()
    if lg == 'fr':
        bc = Background.objects.filter(pk__in=[1,2,6])
        for OneCandidate in the_candidates:
            back_dict=[]
            extras = OneCandidate.backgroundcandidate_set.filter(background__in=bc).order_by('background__id')
            result = ""
            for extra in extras:
                result += normalize_newlines(extra.value).replace('\n', ' ')+u" "
                back_dict.append(extra.value)
            candidat_dict={'label': OneCandidate.name+u" "+mark_safe(result), 'ville':back_dict[1], 'parti':back_dict[0], 'commission':back_dict[2],
            'name': OneCandidate.name, 'value': OneCandidate.slug}
            list_candidat.append(candidat_dict)
    else:
        bc = Background.objects.filter(pk__in=[10,11,15,19])
        for OneCandidate in the_candidates:
            back_dict=[]
            extras = OneCandidate.backgroundcandidate_set.filter(background__in=bc).order_by('background__id')
            result = ""
            for extra in extras:
                result += normalize_newlines(extra.value).replace('\n', ' ')+u" "
                back_dict.append(extra.value)
            candidat_dict={'label': back_dict[3]+u" "+mark_safe(result), 'ville':back_dict[1], 'parti':back_dict[0], 'commission':back_dict[2],
            'name': back_dict[3], 'value': OneCandidate.slug}
            list_candidat.append(candidat_dict)
    return HttpResponse(json.dumps(list_candidat), mimetype="application/json")

def the_candidates(request):
    lelection = Election.objects.get(name='Marruecos2014')
    the_candidates = lelection.can_election.candidate_set.all()
    bc = Background.objects.filter(name__in=['Parti politique','Commission','Circonscription'])
    list_candidat =[]
    for OneCandidate in the_candidates:
        back_dict=[]
        extras = OneCandidate.backgroundcandidate_set.filter(background__in=bc).order_by('background__name')
        result = ""
        for extra in extras:
            result += normalize_newlines(extra.value).replace('\n', ' ')+u" "
            back_dict.append(extra.value)
        candidat_dict={'label': OneCandidate.name+u" "+mark_safe(result), 'ville':back_dict[0], 'parti':back_dict[2], 'commission':back_dict[1],
        'name': OneCandidate.name, 'value': OneCandidate.slug}
        list_candidat.append(candidat_dict)
    return HttpResponse(json.dumps(list_candidat), mimetype="application/json")



#home pour new template	v2	
class Home3View(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(Home3View, self).get_context_data(**kwargs)
        context['election'] = Election.objects.get(slug = "marruecos2014")
        context['writeitmessages'] = VotaInteligenteMessage.objects.filter(writeitinstance=context['election'].writeitinstance, moderated=True, answers__isnull = False).prefetch_related('answers').order_by('-answers__created')[:3]
        context['questions'] = VotaInteligenteMessage.objects.filter(writeitinstance=context['election'].writeitinstance, answers__isnull= True, moderated=True).order_by('-moderated_at')[:5]
        context['top_vote'] = VotaInteligenteMessage.objects.filter(writeitinstance=context['election'].writeitinstance, answers__isnull=True, moderated=True).order_by('-total_upvotes')[:5]
        lg=translation.get_language()
        if lg == 'fr':
            context['backgrounds'] = Background.objects.filter(pk__in=[1,2,6])
        else:
            context['backgrounds'] = Background.objects.filter(pk__in=[10,11,15,19]).order_by('id')
            context['background_name'] = context['backgrounds'][3]
        context['canreachable'] = context['election'].can_election.candidate_set.filter(relation__reachable=True).order_by('name')
        context['question_a'] = _(u"Question à")+ " "
        context['reponse_par'] = _(u"Réponse par")+ " "
        context['sur']= " "+_(u"sur")+" "
        return context		

#depute v1
class ElectionDeputeView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(ElectionDeputeView, self).get_context_data(**kwargs)
        marueccos = Election.objects.get(slug = "marruecos2014")
        context['deputes'] = marueccos.can_election.candidate_set.all().order_by('photo')
        context['slug_election']='marruecos2014'
        context['background'] = Background.objects.filter(Q(name__icontains="Parti politique") | Q(name="Circonscription")).order_by('-name')
        return context		


#profil
class ProfilDetailView(DetailView):
    model = Candidate

    def get_queryset(self):
        queryset = super(ProfilDetailView, self).get_queryset()
        queryset = queryset.filter(election__slug="marruecos2014") #self.kwargs['election_slug']

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProfilDetailView, self).get_context_data(**kwargs)
        #I know this is weird but this is basically
        #me the candidate.candideitorg_election.votainteligente_election
        #so that's why it says election.election
        l_election = self.object.election.election
        context['writeitmessages'] = VotaInteligenteMessage.objects.filter(people=self.object.relation.person, moderated=True).prefetch_related('answers').order_by('-moderated_at')
        context['question_a'] = _(u"Question à")+ " "
        context['reponse_par'] = _(u"Réponse par")+ " "
        context['sur']= " "+_(u"sur")+" "
        lg=translation.get_language()
        if lg == 'fr':
            context['background_categories']=l_election.can_election.backgroundcategory_set.filter(Q(name__icontains="Information") | Q(name__icontains="Affiliation")).order_by('-name')
            context['personal_datas']=l_election.can_election.personaldata_set.all()
        else:
            context['background_categories']=l_election.can_election.backgroundcategory_set.filter(id__in=[3,4]).order_by('id')
            context['personal_data_ar'] = Background.objects.filter(background_category_id = 5).order_by('id')
            context['name_background_pers'] = context['personal_data_ar'][0]
            context['background_name'] = Background.objects.get(pk=19)
        return context		


#question v2
class ElectionQuestionView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(ElectionQuestionView, self).get_context_data(**kwargs)
        context['election'] = Election.objects.get(slug = "marruecos2014")
        context['writeitmessages'] = VotaInteligenteMessage.objects.filter(writeitinstance=context['election'].writeitinstance, moderated=True, answers__isnull = False).prefetch_related('answers').order_by('-answers__created')
        lg=translation.get_language()
        if lg != 'fr':
            context['background_name'] = Background.objects.get(pk=19)
        context['question_a'] = _(u"Question à")+ " "
        context['reponse_par'] = _(u"Réponse par")+ " "
        context['sur']= " "+_(u"sur")+" "
        if self.kwargs['success'] is not None and self.kwargs['success'] == 'succes':
            context['message_done'] = self.kwargs['success']
        return context
		

#Posez 
class ElectionPosezView(CreateView):
		
    model = Message
    form_class = QuestionFormV2
    #initial = {'people': '2'}

    def get_context_data(self, **kwargs):
        context = super(ElectionPosezView, self).get_context_data(**kwargs)
        #self.initial = {'people': self.kwargs['pk']}
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(ElectionPosezView, self).get_form_kwargs()
        election = Election.objects.get(slug = "marruecos2014")
        kwargs['election'] = election
        #kwargs['initial']={'people':'2'}
        return kwargs

    def get_success_url(self):
        return reverse('question_view', kwargs={'success':'succes',})

    def get_initial(self, **kwargs):
        par_defaut={}
        if self.kwargs['pk'] is not None:
            the_pk=self.kwargs['pk']
            par_defaut={'people':[the_pk,],}
        return par_defaut
	
#MessageView
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
        context['question_a'] = _(u"Question à")+ " "
        context['reponse_par'] = _(u"Réponse par")+ " "
        context['sur']= " "+_(u"sur")+" "
        lg=translation.get_language()
        if lg != 'fr':
            context['background_name'] = Background.objects.get(pk=19)
        return context



def deputesview(request):
    marueccos = Election.objects.get(slug = "marruecos2014")
    slug_election='marruecos2014'
    lg = translation.get_language()
    if lg == 'fr':
        background = Background.objects.filter(pk__in=[1,2,6]).order_by('id')
    else:
        background = Background.objects.filter(id__in=[10,11,15,19]).order_by('id')
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
                bg_id_list=[1,2,3,6]
            else:
                bg_id_list=[10,11,12,15]
            deputes = marueccos.can_election.candidate_set
            if nom_mp:
                if lg == 'fr':
                    deputes = deputes.filter(name__icontains=nom_mp)
                else:
                    deputes = deputes.filter(backgroundcandidate__value__contains=nom_mp, backgroundcandidate__background_id=19)
                ok = ok + 1
            if parti:
                deputes = deputes.filter(backgroundcandidate__value = parti, backgroundcandidate__background_id=bg_id_list[0])
                ok = ok + 1
            if circpt:
                deputes = deputes.filter(backgroundcandidate__value =circpt, backgroundcandidate__background_id=bg_id_list[1])
                ok = ok + 1
            if pref_prov:
                deputes = deputes.filter(backgroundcandidate__value =pref_prov, backgroundcandidate__background_id=bg_id_list[2])
                ok = ok + 1
            if commission:
                deputes = deputes.filter(backgroundcandidate__value =commission, backgroundcandidate__background_id=bg_id_list[3])
                ok = ok + 1
            if ok == 0:
			    deputes = deputes.all()
            deputes = deputes.order_by('-relation__reachable', 'name')
        else:
            msg = 'recherche invalide'
            nom_error = form.errors['nom_depute']
        return render(request, 'elections/depute_html.html',locals())
    elif request.method == 'GET' and 's' not in request.GET and 'page' in request.GET:
        deputes = marueccos.can_election.candidate_set.all().order_by('-relation__reachable', 'name')
        return render(request, 'elections/depute_html.html',locals())
    else:
        form = DeputeSearchForm()
        #.values('value')
        deputes = marueccos.can_election.candidate_set.all().order_by('-relation__reachable', 'name')
    return render(request, 'elections/deputes.html',locals())

#ajax for page questions
def ajax_question_view(request):
    mess_content = 'Aucune Question'
    if request.method == 'GET' and 'page' in request.GET and 'genre' in request.GET:
        question_a = _(u"Question à")+ " "
        reponse_par = _(u"Réponse par")+" "
        sur= " "+_(u"sur")+" "
        lg=translation.get_language()
        if lg != 'fr':
            background_name = Background.objects.get(pk=19)
        election = Election.objects.get(slug = "marruecos2014")
        if request.GET['genre'] == '#qa':
            the_qa = VotaInteligenteMessage.objects.filter(writeitinstance=election.writeitinstance, moderated=True, answers__isnull = False).prefetch_related('answers').order_by('-answers__created')
        elif request.GET['genre'] == '#recent':
            recents = VotaInteligenteMessage.objects.filter(writeitinstance=election.writeitinstance, answers__isnull= True, moderated=True).order_by('-moderated_at')
        elif request.GET['genre'] == '#popular':
            populars = VotaInteligenteMessage.objects.filter(writeitinstance=election.writeitinstance, answers__isnull=True, moderated=True).order_by('-total_upvotes')
        else:
            message = mess_content
    else:
        message = mess_content   
    return render(request, 'elections/question_html.html', locals())

#ajax for profil questions
def ajax_profil_question_view(request):
    mess_content = _(u'Aucune Question')
    if request.method == 'GET' and 'page' in request.GET and 'depute' in request.GET and request.GET['depute'].isdigit():
        try:
            candidate=Candidate.objects.get(pk=request.GET['depute'])
            messagesprofil = VotaInteligenteMessage.objects.filter(people=candidate.relation.person, moderated=True).prefetch_related('answers').order_by('-moderated_at')
            lg=translation.get_language()
            if lg != 'fr':
                background_name = Background.objects.get(pk=19)
            question_a = _(u"Question à")+ " "
            reponse_par = _(u"Réponse par")+" "
            sur= " "+_(u"sur")+" "
        except ObjectDoesNotExist:
            message = mess_content
    else:
        message = mess_content
    return render(request, 'elections/profil_question.html', locals())		
