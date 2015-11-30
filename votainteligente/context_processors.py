# coding=utf-8
from django.utils.translation import ugettext as _

def get_url_base(request):
	if request.is_secure():
		scheme = 'https://'
	else:
		scheme = 'http://'
	return {'url_base' : scheme + request.get_host(),}

def word_i18n(request):
	context_extras = {}
	
	context_extras['question_a'] = _(u"Question à") + " "
	context_extras['reponse_par'] = _(u"Réponse par") + " "
	context_extras['sur'] = " " + _(u"sur") + " "
	context_extras['publication_de'] = _(u"Publication de") + " "
	context_extras['cliquez_ici'] = _(u"Nouveau compte député")
	context_extras['mot_de_passe'] = _(u"Mot de passe oublié")
	#this dictionnary is not used in the code just to avoid the fuzzy problem in po file
	tag_extras = {}
	tag_extras['affaires-administratives'] = _(u"Affaires Administratives")
	tag_extras['economie'] = _(u"Affaires Etrangères")
	tag_extras['economie'] = _(u"Affaires Islamiques")
	tag_extras['economie'] = _(u"Agriculture")
	tag_extras['economie'] = _(u"Artisanat")
	tag_extras['economie'] = _(u"Collectivités territoriales")
	tag_extras['economie'] = _(u"Commerce")
	tag_extras['economie'] = _(u"Communication")
	tag_extras['economie'] = _(u"Culture")
	tag_extras['economie'] = _(u"Défense Nationale")
	tag_extras['economie'] = _(u"Développement Durable")
	tag_extras['economie'] = _(u"Développement Economique")
	tag_extras['economie'] = _(u"Développement Rural")
	tag_extras['economie'] = _(u"Droits de l'homme")
	tag_extras['economie'] = _(u"Économie")
	tag_extras['education'] = _(u"Éducation")
	tag_extras['economie'] = _(u"Emploi")
	tag_extras['economie'] = _(u"Énergie")
	tag_extras['economie'] = _(u"Enseignement Supérieur")
	tag_extras['economie'] = _(u"Environnement")
	tag_extras['economie'] = _(u"Equipement")
	tag_extras['economie'] = _(u"Famille")
	tag_extras['economie'] = _(u"Femme")
	tag_extras['economie'] = _(u"Finance")
	tag_extras['economie'] = _(u"Fonction publique")
	tag_extras['economie'] = _(u"Formation Professionnelle")
	tag_extras['economie'] = _(u"Gouvernance")
	tag_extras['economie'] = _(u"Habitat")
	tag_extras['economie'] = _(u"Handicap")
	tag_extras['economie'] = _(u"Industrie")
	tag_extras['economie'] = _(u"Infrastructures")
	tag_extras['economie'] = _(u"Institutions Publiques")
	tag_extras['economie'] = _(u"Intérieur")
	tag_extras['economie'] = _(u"Investissement")
	tag_extras['economie'] = _(u"Jeunesse")
	tag_extras['economie'] = _(u"Justice")
	tag_extras['economie'] = _(u"Législation")
	tag_extras['economie'] = _(u"Marocains Résidant à l'Étranger")
	tag_extras['economie'] = _(u"Media")
	tag_extras['economie'] = _(u"Nouvelles Technologies")
	tag_extras['economie'] = _(u"Parlement")
	tag_extras['economie'] = _(u"Pêche")
	tag_extras['economie'] = _(u"Politique de la Ville")
	tag_extras['economie'] = _(u"Ressources Humaines")
	tag_extras['economie'] = _(u"Ressources Naturelles")
	tag_extras['economie'] = _(u"Retraite")
	tag_extras['economie'] = _(u"Santé")
	tag_extras['economie'] = _(u"Secteurs Productifs")
	tag_extras['economie'] = _(u"Secteurs sociaux")
	tag_extras['economie'] = _(u"Société Civile")
	tag_extras['economie'] = _(u"Solidarité")
	tag_extras['economie'] = _(u"Sport")
	tag_extras['economie'] = _(u"Tourisme")
	tag_extras['economie'] = _(u"Transport")

	return context_extras
