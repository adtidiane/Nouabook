from django import template

register = template.Library()

from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from elections.models import Election
import simplejson as json
from django.conf import settings
from django.contrib.sites.models import Site
#from candideitorg.models import BackgroundCandidate
from django.utils.translation import ugettext as _
import re

@register.simple_tag
def elections_json():
	expected_elections = []
	for election in Election.objects.filter(searchable=True):
		tags = []
		for tag in election.tags.all():
			tags.append(tag.name)

		election_dict = {
		'name': election.name,
		'slug': election.slug,
		'detaillink':election.get_absolute_url(),
		'tags':tags
		}
		expected_elections.append(election_dict)
	return mark_safe(json.dumps(expected_elections))

@register.filter
def val_navbars(section):
	if section in settings.NAV_BAR:
		return True

@register.simple_tag
def title(election, name):	
	return election + ' - ' + name;

@register.simple_tag
def url_domain():
    return Site.objects.get_current().domain

@register.filter
def metadata(meta):
	if meta in settings.WEBSITE_METADATA:
		return settings.WEBSITE_METADATA[meta]
	return ''

@register.filter
def ogpdata(ogp):
	if ogp in settings.WEBSITE_OGP:
		return settings.WEBSITE_OGP[ogp]
	return ''

@register.filter
def disqus(disqus):
	if disqus in settings.WEBSITE_DISQUS:
		return settings.WEBSITE_DISQUS[disqus]
	return ''

@register.filter
def ga(value):
	if value in settings.WEBSITE_GA:
		return settings.WEBSITE_GA[value]
	return ''

@register.filter
def fbsetting(item):
    if item in settings.WEBSITE_FACEBOOK:
        return settings.WEBSITE_FACEBOOK[item]
    return ''

def no_ha_respondido_twitter_button(context):
	twitter = context["candidate"].relation.twitter
	if twitter:
		context["twitter"] = twitter
		return context
	context["twitter"] = None
	return context
register.inclusion_tag('elections/twitter/no_candidator_answer.html', 
	takes_context=True)(no_ha_respondido_twitter_button)


def follow_on_twitter(context):
	twitter = context["candidate"].relation.twitter
	if twitter:
		context["twitter"] = twitter
		return context
	context["twitter"] = None
	return context
register.inclusion_tag('elections/twitter/follow_the_conversation.html', 
	takes_context=True)(follow_on_twitter)

@register.filter
#website general settings
def website_gs(value):
	if value in settings.WEBSITE_GENERAL_SETTINGS:
		return settings.WEBSITE_GENERAL_SETTINGS[value]
	return ''

@register.filter
#website general settings
def website_imgur(value):
	if value in settings.WEBSITE_IMGUR:
		return settings.WEBSITE_IMGUR[value]
	return ''

def twitter_on_ranking(context,btn_text,popup_text):
	twitter = context["candidate"].relation.twitter
	if twitter:
		return {
			'twitter':twitter,
			'candidate':context['candidate'],
			'btn_text' : btn_text,
			'popup_text' : popup_text
			}
	return {
		'twitter':None,
		'candidate':context['candidate'],
		'btn_text' : btn_text,
		'popup_text' : popup_text
		}

register.inclusion_tag('elections/twitter/ranking_twitter.html', takes_context=True)(twitter_on_ranking)

@register.filter
#website general settings
def website_twitter(value):
	if value in settings.WEBSITE_TWITTER:
		return settings.WEBSITE_TWITTER[value]
	return ''

@register.simple_tag
def r_candidate_background(candidate, background):
    try:
        valeur = background.backgroundcandidate_set.get(candidate=candidate).value
        if len(valeur):
            return valeur
        else:
            return _('indisponible')
    except:
        return _('aucun')

from django.db.models import Q
from django.utils.text import normalize_newlines
from candideitorg.models import Background
@register.simple_tag
def candidate_extra(candidate):
    try:
        bc = Background.objects.filter(Q(name__icontains="Parti politique") | Q(name="Circonscription"))
        extras = candidate.backgroundcandidate_set.filter(background__in=bc)
        result = ""
        for extra in extras:
            result += u" " + normalize_newlines(extra.value).replace('\n', ' ')
        return mark_safe(result)
    except Exception, e:
        return e.message

@register.simple_tag
def r_personal_data_candidate(candidate, personaldata):
    try:
        valeur = personaldata.personaldatacandidate_set.get(candidate=candidate).value
        if len(valeur):
            return valeur
        else:
            return _('indisponible')
    except:
        return _('aucun')		

@register.filter
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)
