# encoding=utf-8

from django.contrib import admin
from elections.models import Election, VotaInteligenteMessage, VotaInteligenteAnswer, CandidatePerson
from flatpages_i18n.admin import FlatpageForm, FlatPageAdmin
from flatpages_i18n.models import FlatPage_i18n
## OOPS this is a custom widget that works for initializing
## tinymce instances on stacked and tabular inlines
## for flatpages, just use the tinymce packaged one.
#from content.widgets import TinyMCE
from tinymce.widgets import TinyMCE
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html
from django.http import HttpResponse
from elections.encoder_csv import UnicodeReader, UnicodeWriter
from secretballot.models import Vote
from django.core.urlresolvers import reverse
from django.contrib.auth import admin as adminpy
from elections.forms import UserCreationForm2
from django.contrib.auth.models import User
from south.models import MigrationHistory


class ElectionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'tags']
	
admin.site.register(Election, ElectionAdmin)

class PageForm(FlatpageForm):

    class Meta:
        model = FlatPage_i18n #FlatPage
        widgets = {
            #'content' : TinyMCE(),
		    'content_fr' : TinyMCE(),
            'content_ar' : TinyMCE(),
        }

class PageAdmin(FlatPageAdmin):
    """
    Page Admin
    """
    form = PageForm

admin.site.unregister(FlatPage_i18n)
admin.site.register(FlatPage_i18n, PageAdmin)

class AnswerInline(admin.TabularInline):
    model = VotaInteligenteAnswer
    fields = ['content','person','number_votes_answer']
    readonly_fields = ('number_votes_answer',)
    extra = 0

    def number_votes_answer(self, answer):
        return format_html('<span style="font-size:13px">%d</span>' % (answer.total_upvotes,))
    number_votes_answer.short_description = 'number votes'

class CandidatePersonExtraInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('person',)
    fields = ('reachable','description', 'portrait_photo', 'custom_ribbon', 'canUsername', 'tags')
    search_fields = ['person__name', 'person__api_instance__election__name']

admin.site.register(CandidatePerson, CandidatePersonExtraInfoAdmin)


class MensajesAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'number_votes',)
    fields = ['author_name','author_email', 'subject', 'content', 'author_ville', 'people', 'tags', 'created', 'number_votes', 'pending_status', 'rejected_status', 'moderated', 'fbshared', 'is_video']
    list_filter = ('moderated', 'rejected_status', 'pending_status',)
    search_fields = ['author_name', 'author_email', 'subject', 'writeitinstance__name', 'people__name']
    inlines = [
    AnswerInline
    ]
    
    def status_moderation(self):
        html_return=""
        if(self.moderated):
            html_return = '<span class="label label-default">'+u"moderée"+'</span>'
        else:
            html_return = '<span class="label label-warning">'+u"Non moderée"+'</span>'
        return format_html(html_return)

    #function for column pending or rejected status
    def pending_or_rejected(self):
        html_return = ""
        if(self.rejected_status):
            html_return = '<span class="label label-important">'+u"rejetée"+'</span>'
        elif(self.pending_status):
            html_return = '<span class="label label-info">'+u"en attente"+'</span>'
        return format_html(html_return)

    #function for number of votes column
    def number_votes(self, message):
        return message.total_upvotes
    number_votes.short_description = 'Number of votes'
    number_votes.admin_order_field = 'total_upvotes'
	
    list_display = ('author_name', 'author_email', 'subject', 'number_votes', 'created', 'moderated_at', status_moderation, pending_or_rejected)
    ordering = ('moderated','pending_status', 'rejected_status',)
	
    actions = ['charger_stat_csv','accept_moderation',]
    actions_on_top = False
    actions_on_bottom = True

    def accept_moderation(self, request, queryset):
        for message in queryset:
            message.accept_moderation()
    accept_moderation.short_description = "Accepter les messages a envoyer"

    def yes_no(self, value):
        if value is True:
            retour = "yes"
        else:
            retour = "no"
        return retour

    def time_response(self, list_date):
        duree = list_date[1] - list_date[0]
        return str(duree)    
	
    #function to generate CSV file
    def charger_stat_csv(self, request, queryset):
        #with open('rempli_stat.csv', 'wb') as csvfile:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stat_questions.csv"'
        writer = UnicodeWriter(response)
        writer.writerow(['author_name','author_email', 'subject', 'content','author_ville', u'député', 'created date', 'number votes', 'moderated', u'shared facebook', 'has_response',\
		u'response content','date response', 'duration response (days, H:M:S)'])
        for s in queryset:
            created_date = str(s.created);
            str_moderated = self.yes_no(s.moderated)
            str_fbshared = self.yes_no(s.fbshared)
            depute=s.people.all()
            s_answer = s.answers.all()
            if len(s_answer) == 0:
                has_answer = "no"
                answer_content = ""
                answer_date = ""
                time_ms_answ = ""
            else:
                has_answer = "yes"
                answer_content = s_answer[0].content
                answer_date = str(s_answer[0].created)
                time_ms_answ = self.time_response([s.moderated_at, s_answer[0].created])
            writer.writerow([s.author_name, s.author_email, s.subject, s.content, s.author_ville, depute[0].name, created_date, str(s.total_upvotes), str_moderated ,str_fbshared, has_answer,\
			answer_content, answer_date, time_ms_answ]) 
        return response
    charger_stat_csv.short_description = u"Télécharger sous format CSV"

admin.site.register(VotaInteligenteMessage, MensajesAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('vote', 'type_object', 'subject_object', 'token','updated_at',)
    list_filter = ('updated_at','token', )
    ordering = ('-updated_at',)
    actions = ['charger_csv_vote',]
    actions_on_top = False
    actions_on_bottom = True
	
    def type_object(self, levote):
        retour = ''
        if levote.content_object.__class__.__name__ == 'VotaInteligenteMessage':
            retour = '<span class="label">Question</span>'
        elif levote.content_object.__class__.__name__ == 'VotaInteligenteAnswer':
            retour = '<span class="label label-success">Answer</span>'
        return format_html(retour)
    type_object.short_description = 'content type name'
    type_object.admin_order_field = 'content_type'
	
    def subject_object(self, levote):
        retour = ''
        if levote.content_object.__class__.__name__ == 'VotaInteligenteMessage':
            url_object= reverse('admin:elections_votainteligentemessage_change', args=(levote.object_id, ))
            retour = '<a href="%s" target="_blank">%s</a>' % (url_object, levote.content_object.subject, )
        elif levote.content_object.__class__.__name__ == 'VotaInteligenteAnswer':
            url_object= reverse('admin:elections_votainteligentemessage_change', args=(levote.content_object.message.id, ))
            retour = '<a href="%s" target="_blank">%s</a>' % (url_object, levote.content_object.message.subject, )
        return format_html(retour)
    subject_object.short_description = 'Subject'
	
    def charger_csv_vote(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stat_votes.csv"'
        writer = UnicodeWriter(response)
        writer.writerow(['Vote', 'Content type name', 'subject', 'token', 'updated at'])
        for v in queryset:
            v_vote = str(v.vote)
            v_content_type =''
            v_subject = ''
            v_updated_at = str(v.updated_at)
            if v.content_object.__class__.__name__ == 'VotaInteligenteMessage':
                v_content_type = 'Question'
                v_subject = v.content_object.subject
            elif v.content_object.__class__.__name__ == 'VotaInteligenteAnswer':
                v_content_type = 'Answer'
                v_subject = v.content_object.message.subject
            writer.writerow([v_vote,v_content_type, v_subject, v.token, v_updated_at])
        return response
    charger_csv_vote.short_description = u"Télécharger sous format CSV"

admin.site.register(Vote, VoteAdmin)

#test modificiation admin.py de django admin
class UserInAdmin(adminpy.UserAdmin):
    add_form = UserCreationForm2
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email')}
        ),
    )

admin.site.unregister(User)
admin.site.register(User, UserInAdmin)

class MigrationsAdmin(admin.ModelAdmin):
    list_display = ('migration',)

admin.site.register(MigrationHistory, MigrationsAdmin)