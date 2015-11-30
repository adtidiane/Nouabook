# encoding=utf-8
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from haystack.views import SearchView
from elections.forms import ElectionForm
from django.views.generic import DetailView
from elections.models import VotaInteligenteMessage
# from sitemaps import *

from django.conf import settings
from django.views.decorators.cache import cache_page
from elections.views import AnswerWebHook, ElectionQuestionView, ElectionPosezView, ProfilDetailView, MessageView, \
    Home3View, ProfilAccountDetailView, UpdateOrderView, ProfileQuestionView, \
    AnswerQuestionFormView, AnswerQuestionFormViewUpdate, StatusUpdateCreateView, \
    StatusUpdateUpdateView, StatusPosezView, StatusQuestionsView, CitizeTimelineView, ElectionPosezXView, \
    ElectionPosezXTagView

media_root = getattr(settings, 'MEDIA_ROOT', '/')

new_answer_endpoint = r"^new_answer/%s/?$" % (settings.NEW_ANSWER_ENDPOINT)

"""sitemaps = {
    'elections': ElectionsSitemap,
    'candidates': CandidatesSitemap,
}"""

urlpatterns = patterns('',
                       # url(r'^login/$', 'elections.views.login_page', name='login'),
                       url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                       url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login'}, name='logout'),
                       url(r'^update_ranking$', 'elections.views.update_ranking'),

                       # citizen timeline
                       url(r'^publications/?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               CitizeTimelineView.as_view(template_name='elections/citizen_timeline.html')),
                           name='citizen_timeline_view'),

                       # ajax get deputes by tags
                       url(r'^ajax_deputes_tag$', 'elections.views.get_deputes_by_tag', name="ajax_mp_tag_view"),

                       url(new_answer_endpoint, AnswerWebHook.as_view(), name='new_answer_endpoint'),
                       # home3 new template url
                       url(r'^/?$', cache_page(60 * settings.CACHE_MINUTES)(
                           Home3View.as_view(template_name='elections/home3.html')), name='home3_view'),
                       # question_v2
                       url(r'^questions/(?P<success>\w+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               ElectionQuestionView.as_view(template_name='elections/question.html')),
                           name='question_view'),
                       # depute
                       url(r'^deputes/?$', 'elections.views.deputesview', name='depute_view'),
                       # posez
                       url(r'^posez$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               ElectionPosezView.as_view(template_name='elections/posez.html')), name='posez_view'),
                       # posez x
                       url(r'^posez/(?P<pk>\d+)$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               ElectionPosezXView.as_view(template_name='elections/posez_x.html')), name='posez_x_view'),
                       # posez x on tag
                       url(r'^posez/(?P<pk>\d+)-theme-(?P<tag>\d+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               ElectionPosezXTagView.as_view(template_name='elections/posez_x_tag.html')), name='posez_x_tag_view'),
                       # posez status
                       url(r'^posez/(?P<pk>\d+)-status-(?P<status>\d+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               StatusPosezView.as_view(template_name='elections/posez_status.html')), name='posez_status_view'),
                       # voir questions status
                       url(r'^questions-status/(?P<pk>\d+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               StatusQuestionsView.as_view(template_name='elections/questions_status.html')), name='questions_status_view'),
                       # profil_rempli
                       url(r'^profil/(?P<slug>[-\w]+)/?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               ProfilDetailView.as_view(template_name='elections/profil.html')), name='profil_view'),
                       # profil_account
                       url(r'^accounts/profile/?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               ProfilAccountDetailView.as_view()), name='account_profil_view'),                       
                       # profil_account_questions
                       url(r'^accounts/profile/questions/(?P<success>\w+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               ProfileQuestionView.as_view(template_name='elections/account/question.html')),
                           name='account_question_view'),
                       # Account Create answer message
                       url(r'^accounts/profile/questions/message-(?P<pk>\d+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               AnswerQuestionFormView.as_view(template_name='elections/account/repondre_question.html')),
                           name='account_repondre_message_view'),
                       # Account UPDATE answer message
                       url(r'^accounts/profile/questions/update/message-(?P<pk>\d+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               AnswerQuestionFormViewUpdate.as_view(template_name='elections/account/update_reponse_question.html')),
                           name='account_update_repondre_message_view'),
                       # Account add Tag to MP
                       url(r'^accounts/profile/tag_to_mp$', 'elections.views.tag_to_mp', name='add_tag_to_mp'),
                       # Account DELETE answer attachment
                       url(r'^delete_file$', 'elections.views.delete_attachment'),
                       # Account DELETE Status Update
                       url(r'^delete_status$', 'elections.views.delete_status'),
                       # Account Create Status update
                       url(r'^accounts/status/(?P<success>\w+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               StatusUpdateCreateView.as_view(template_name='elections/account/status/index.html')),
                           name='account_status_view'),
                       # Account UPDATE status update
                       url(r'^accounts/status/update/post-(?P<pk>\d+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               StatusUpdateUpdateView.as_view(template_name='elections/account/status/update_status.html')),
                           name='account_status_update_view'),
                       # question contenu 2
                       url(r'^questions/message-(?P<pk>\d+)(?P<reponse>[-\w]+)?$',
                           cache_page(60 * settings.CACHE_MINUTES)(
                               MessageView.as_view(template_name='elections/question_reponse.html')),
                           name='message_view'),
                       url(r'^the_candidatesv2$', 'elections.views.the_candidatesv2', name='candidate_ajax'),
                       # version 2 ajax candidate
                       # vote ajax
                       url(r'^votedirect$', 'elections.views.vote_ajax', name="votedirect"),
                       url(r'^telecharger_csv$', 'elections.views.charger_csv', name="charger_csv"),
                       # question load ajax
                       url(r'^questions_load/$', 'elections.views.ajax_question_view', name='question_ajax'),
                       # profil question ajax
                       url(r'^profil_questions_load/$', 'elections.views.ajax_profil_question_view',
                           name='profil_question_ajax'),
                       url(r'^profil_questions_backend_load/$', 'elections.views.ajax_profil_question_backend', name='profil_question_ajax_backend'),
                       # load tumbl api
                       url(r'^blog_load/$', 'elections.views.blog_ajax_view', name='blog_ajax'),
                       # url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
                       )

urlpatterns += patterns('',
                        url(r'^cache/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': media_root})
                        )
