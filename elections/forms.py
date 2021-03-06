# coding=utf-8
from haystack.forms import SearchForm
from django import forms
from django.forms import ModelForm, CheckboxSelectMultiple, Select, SelectMultiple, ModelMultipleChoiceField
from django.utils.translation import ugettext as _, get_language
from elections.models import Election, VotaInteligenteMessage
from candideitorg.models import BackgroundCandidate as Backcan, Background, Candidate

class ElectionForm(SearchForm):
	pass

class ElectionSearchByTagsForm(forms.Form):
	q = forms.CharField(required=False, label=_('Busca tu comuna'))

	def get_search_result(self):
		cleaned_data = self.clean()
		queryed_element = cleaned_data['q']
		return Election.objects.filter(tags__name__in=[queryed_element])


class MessageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election')
        self.writeitinstance = self.election.writeitinstance
        super(MessageForm, self).__init__(*args, **kwargs)
        self.instance.writeitinstance = self.writeitinstance
        self.instance.api_instance = self.writeitinstance.api_instance
        self.fields['people'].queryset = self.election.popit_api_instance.person_set.filter(relation__reachable=True)

    class Meta:
        model = VotaInteligenteMessage
        fields = ('author_name', 'author_email', 'subject', 'content','people','author_ville', 'fbshared')
        widgets = {
            'people': CheckboxSelectMultiple(),
        }
        labels = {
            'author_name': _('Nombre'),
            'author_email': _(u'Correo electrónico'),
            'subject': _('Asunto'),
            'content': _('texto'),
            'people': _('Destinatarios'),
        }
        help_texts = {
            'people': _(u'Puedes seleccinar a más de un candidato para dirigir tu pregunta'),
            'author_name': _(u'Identíficate de alguna forma: Estudiante, Obrero, Democrático, Dirigente, etc.'),
        }
        error_messages = {
            'name': {
                'required': _('Debes identificarte de alguna forma.'),
            },
        }

class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election')
        self.writeitinstance = self.election.writeitinstance
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.instance.writeitinstance = self.writeitinstance
        self.instance.api_instance = self.writeitinstance.api_instance
        self.fields['people'].queryset = self.election.popit_api_instance.person_set.filter(relation__reachable=True).order_by('name')

    class Meta:
        model = VotaInteligenteMessage
        fields = ('author_name', 'author_email', 'subject', 'content','people','fbshared')
        widgets = {
            'people': SelectMultiple(attrs={'class':'chosen-select','data-placeholder':'votre députée/député', 'style':'width:40%;'})
        }
        labels = {
            'author_name': _('Nombre'),
            'author_email': _(u'Correo electrónico'),
            'subject': _('Asunto'),
            'content': _('texto'),
            'people': _('Destinatarios'),
        }
        help_texts = {
            'people': _(u'Puedes seleccinar a más de un candidato para dirigir tu pregunta'),
            'author_name': _(u'Identíficate de alguna forma: Estudiante, Obrero, Democrático, Dirigente, etc.'),
        }
        error_messages = {
            'name': {
                'required': _('Debes identificarte de alguna forma.'),
            },
        }

class MyModelMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        candidate_pers = Backcan.objects.get(background_id=19, candidate=obj.relation.candidate)
        return candidate_pers.value
		
class QuestionFormV2(ModelForm):

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election')
        self.writeitinstance = self.election.writeitinstance
        super(QuestionFormV2, self).__init__(*args, **kwargs)
        self.instance.writeitinstance = self.writeitinstance
        self.instance.api_instance = self.writeitinstance.api_instance
        #self.fields['people'].queryset = self.election.popit_api_instance.person_set.filter(relation__reachable=True).order_by('name')
        lg = get_language()
        if lg == 'fr':
            self.fields['people'] = ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'chosen-select', 'style':'width:100%;',}), queryset=self.election.popit_api_instance.person_set.filter(relation__reachable=True).order_by('name'))
        else:
            self.fields['people'] = MyModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':'chosen-select', 'style':'width:100%;',}), queryset=self.election.popit_api_instance.person_set.filter(relation__reachable=True).order_by('id'))

    class Meta:
        model = VotaInteligenteMessage
        fields = ('author_name', 'author_email', 'subject', 'content','people','fbshared','author_ville','is_video')
        """widgets = {
            'people': SelectMultiple(attrs={'class':'chosen-select', 'style':'width:100%;'})
        }"""
        labels = {
            'author_name': _('Nombre'),
            'author_email': _(u'Correo electrónico'),
            'subject': _('Asunto'),
            'content': _('texto'),
            'people': _('Destinatarios'),
        }
        help_texts = {
            'people': _(u'Puedes seleccinar a más de un candidato para dirigir tu pregunta'),
            'author_name': _(u'Identíficate de alguna forma: Estudiante, Obrero, Democrático, Dirigente, etc.'),
        }
        error_messages = {
            'name': {
                'required': _('Debes identificarte de alguna forma.'),
            },
        }
		
class NewsletterForm(forms.Form):
    nom_sender = forms.CharField(max_length=100)
    email_sender = forms.EmailField(label=u"Votre adresse mail")


class DeputeSearchForm(forms.Form):
    def my_choices(id):
        noms=Backcan.objects.filter(background_id=id).values('value').order_by('value').distinct()
        my_list = [('','Tous')]
        for n in noms:
		    my_list.append((n['value'], n['value']))
        return my_list

    def my_choices_ar(self,id):
        noms=Backcan.objects.filter(background_id=id).values('value').order_by('value').distinct()
        my_list = [('','جميع الاختيارات')]
        for n in noms:
		    my_list.append((n['value'], n['value']))
        return my_list

    def my_choice_mp(self):
        mps=Candidate.objects.all().values('name').order_by('name')
        my_list= [('','')]
        for n in mps:
		    my_list.append((n['name'], n['name']))
        return my_list
		
    def my_choice_mp_ar(self):
        mps=Backcan.objects.filter(background_id=19).values('value')
        my_list= [('','')]
        for n in mps:
		    my_list.append((n['value'], n['value']))
        return my_list
		
    s=forms.CharField(widget=forms.HiddenInput, required=True, initial='search')
    #nom_depute = forms.CharField(max_length=100, min_length=3, required=False)
    parti_politique = forms.ChoiceField(widget=forms.Select, choices=my_choices(1), required=False)
    circonscription = forms.ChoiceField(widget=forms.Select, choices=my_choices(2), required=False)
    pref_or_prov = forms.ChoiceField(widget=forms.Select, choices=my_choices(3), required=False)
    commission = forms.ChoiceField(widget=forms.Select, choices=my_choices(6), required=False)

    def __init__(self, *args, **kwargs):
        lg=get_language()
        super(DeputeSearchForm, self).__init__(*args, **kwargs)
        """self.fields['nom_depute'].error_messages={'min_length':_(u'Saisissez les 3 premières lettres du nom'),}
        self.fields['nom_depute'].widget = forms.TextInput(attrs={'placeholder':_(u'Saisissez les 3 premières lettres du nom'),})"""
        if lg == 'ar':
            self.fields['parti_politique'].choices=self.my_choices_ar(10)
            self.fields['circonscription'].choices=self.my_choices_ar(11)
            self.fields['pref_or_prov'].choices=self.my_choices_ar(12)
            self.fields['commission'].choices=self.my_choices_ar(15)
            self.fields['nom_depute'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'chosen-select chosen-rtl','style':'width:40%;',}), choices=self.my_choice_mp_ar(), required=False)	
        else:
            self.fields['nom_depute'] = forms.ChoiceField(widget=forms.Select(attrs={'class':'chosen-select','style':'width:40%;',}), choices=self.my_choice_mp(), required=False)
