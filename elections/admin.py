# coding=utf-8
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

class ElectionAdmin(admin.ModelAdmin):
    search_fields = ['name', 'tags']
	
admin.site.register(Election, ElectionAdmin)

class PageForm(FlatpageForm):

    class Meta:
        model = FlatPage_i18n 
        widgets = {
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
    fields = ['content','person']
    extra = 0

class CandidatePersonExtraInfoAdmin(admin.ModelAdmin):
    readonly_fields = ('person',)
    fields = ('reachable','description', 'portrait_photo', 'custom_ribbon')
    search_fields = ['person__name', 'person__api_instance__election__name']

admin.site.register(CandidatePerson, CandidatePersonExtraInfoAdmin)


class MensajesAdmin(admin.ModelAdmin):
    fields = ['author_name','author_email', 'subject', 'content', 'people', 'moderated']
    list_filter = ('moderated', )
    search_fields = ['author_name', 'author_email', 'subject', 'writeitinstance__name', 'people__name']
    inlines = [
    AnswerInline
    ]

    actions = ['accept_moderation']

    def accept_moderation(self, request, queryset):
        for message in queryset:
            message.accept_moderation()
    accept_moderation.short_description = "Aceptar Mensajes para ser enviados"

admin.site.register(VotaInteligenteMessage, MensajesAdmin)