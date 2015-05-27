from django.conf import settings
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from haystack.views import SearchView
from elections.forms import ElectionForm
from django.views.generic import DetailView
from elections.models import VotaInteligenteMessage
from sitemaps import *

from django.conf import settings
from django.views.decorators.cache import cache_page
from elections.views import AnswerWebHook,ElectionQuestionView, ElectionPosezView,ProfilDetailView,MessageView,Home3View

media_root = getattr(settings, 'MEDIA_ROOT', '/') 

new_answer_endpoint = r"^new_answer/%s/?$" % (settings.NEW_ANSWER_ENDPOINT)

sitemaps = {
    'elections': ElectionsSitemap,
    'candidates': CandidatesSitemap,
}

urlpatterns = patterns('',
	url(new_answer_endpoint,AnswerWebHook.as_view(), name='new_answer_endpoint' ),
    #home3 new template url
    url(r'^/?$', cache_page(60 * settings.CACHE_MINUTES)(Home3View.as_view(template_name='elections/home3.html')), name='home3_view'),
    #question_v2
    url(r'^questions/(?P<success>\w+)?$',
		cache_page(60 * settings.CACHE_MINUTES)(ElectionQuestionView.as_view(template_name='elections/question.html')), name='question_view'),
    #depute
    url(r'^deputes/?$', 'elections.views.deputesview', name='depute_view'),
    #posez
    url(r'^posez/(?P<pk>\d+)?$',
		cache_page(60 * settings.CACHE_MINUTES)(ElectionPosezView.as_view(template_name='elections/posez.html')), name='posez_view'),
    #profil_rempli
    url(r'^profil/(?P<slug>[-\w]+)/?$',
		cache_page(60 * settings.CACHE_MINUTES)(ProfilDetailView.as_view(template_name='elections/profil.html')), name='profil_view'),
    #question contenu 2
    url(r'^questions/message-(?P<pk>\d+)(?P<reponse>[-\w]+)?$',
		cache_page(60 * settings.CACHE_MINUTES)(MessageView.as_view(template_name='elections/question_reponse.html')), name='message_view'),
    url(r'^the_candidatesv2$', 'elections.views.the_candidatesv2', name='candidate_ajax'), #version 2 ajax candidate
    #vote ajax
    url(r'^votedirect$', 'elections.views.vote_ajax', name="votedirect"), 
    url(r'^telecharger_csv$', 'elections.views.charger_csv', name="charger_csv"),
    #question load ajax
    url(r'^questions_load/$', 'elections.views.ajax_question_view', name='question_ajax'),
    #profil question ajax
    url(r'^profil_questions_load/$', 'elections.views.ajax_profil_question_view', name='profil_question_ajax'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

urlpatterns += patterns('', 
	url(r'^cache/(?P<path>.*)$','django.views.static.serve',
    	{'document_root': media_root})
)
