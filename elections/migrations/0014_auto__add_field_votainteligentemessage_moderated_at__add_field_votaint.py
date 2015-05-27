# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'VotaInteligenteMessage.moderated_at'
        db.add_column(u'elections_votainteligentemessage', 'moderated_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'VotaInteligenteMessage.first_moderation'
        db.add_column(u'elections_votainteligentemessage', 'first_moderation',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'VotaInteligenteMessage.pending_status'
        db.add_column(u'elections_votainteligentemessage', 'pending_status',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'VotaInteligenteMessage.rejected_status'
        db.add_column(u'elections_votainteligentemessage', 'rejected_status',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'VotaInteligenteMessage.moderated_at'
        db.delete_column(u'elections_votainteligentemessage', 'moderated_at')

        # Deleting field 'VotaInteligenteMessage.first_moderation'
        db.delete_column(u'elections_votainteligentemessage', 'first_moderation')

        # Deleting field 'VotaInteligenteMessage.pending_status'
        db.delete_column(u'elections_votainteligentemessage', 'pending_status')

        # Deleting field 'VotaInteligenteMessage.rejected_status'
        db.delete_column(u'elections_votainteligentemessage', 'rejected_status')


    models = {
        u'candideitorg.answer': {
            'Meta': {'object_name': 'Answer'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['candideitorg.Question']"}),
            'remote_id': ('django.db.models.fields.IntegerField', [], {}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'candideitorg.candidate': {
            'Meta': {'object_name': 'Candidate'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['candideitorg.Answer']", 'null': 'True', 'blank': 'True'}),
            'election': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['candideitorg.Election']"}),
            'has_answered': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.IntegerField', [], {}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'candideitorg.category': {
            'Meta': {'object_name': 'Category'},
            'election': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['candideitorg.Election']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'remote_id': ('django.db.models.fields.IntegerField', [], {}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        u'candideitorg.election': {
            'Meta': {'object_name': 'Election'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'information_source': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'remote_id': ('django.db.models.fields.IntegerField', [], {}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'use_default_media_naranja_option': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'candideitorg.question': {
            'Meta': {'object_name': 'Question'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['candideitorg.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'remote_id': ('django.db.models.fields.IntegerField', [], {}),
            'resource_uri': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'elections.candidateperson': {
            'Meta': {'object_name': 'CandidatePerson'},
            'candidate': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'relation'", 'unique': 'True', 'to': u"orm['candideitorg.Candidate']"}),
            'custom_ribbon': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'relation'", 'unique': 'True', 'to': u"orm['popit.Person']"}),
            'portrait_photo': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'reachable': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elections.election': {
            'Meta': {'object_name': 'Election'},
            'can_election': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['candideitorg.Election']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'extra_info_content': ('django.db.models.fields.TextField', [], {'max_length': '3000', 'null': 'True', 'blank': 'True'}),
            'extra_info_title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'highlighted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'popit_api_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['popit.ApiInstance']", 'null': 'True', 'blank': 'True'}),
            'searchable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique': 'True', 'max_length': '50', 'populate_from': "'name'", 'unique_with': '()'}),
            'uses_face_to_face': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uses_preguntales': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uses_questionary': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uses_ranking': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'uses_soul_mate': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'writeitinstance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['writeit.WriteItInstance']", 'null': 'True', 'blank': 'True'})
        },
        u'elections.votainteligenteanswer': {
            'Meta': {'object_name': 'VotaInteligenteAnswer'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['elections.VotaInteligenteMessage']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': u"orm['popit.Person']"})
        },
        u'elections.votainteligentemessage': {
            'Meta': {'object_name': 'VotaInteligenteMessage', '_ormbases': [u'writeit.Message']},
            'author_ville': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '35'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fbshared': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_moderation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_video': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'message_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['writeit.Message']", 'unique': 'True', 'primary_key': 'True'}),
            'moderated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'moderated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pending_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rejected_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'popit.apiinstance': {
            'Meta': {'object_name': 'ApiInstance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('popit.fields.ApiInstanceURLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'popit.person': {
            'Meta': {'object_name': 'Person'},
            'api_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['popit.ApiInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'popit_url': ('popit.fields.PopItURLField', [], {'default': "''", 'max_length': '200', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'writeit.message': {
            'Meta': {'object_name': 'Message', '_ormbases': [u'writeit.WriteItDocument']},
            'author_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'author_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'messages'", 'symmetrical': 'False', 'to': u"orm['popit.Person']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            u'writeitdocument_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['writeit.WriteItDocument']", 'unique': 'True', 'primary_key': 'True'}),
            'writeitinstance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['writeit.WriteItInstance']"})
        },
        u'writeit.writeitapiinstance': {
            'Meta': {'object_name': 'WriteItApiInstance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'writeit.writeitdocument': {
            'Meta': {'object_name': 'WriteItDocument'},
            'api_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['writeit.WriteItApiInstance']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'remote_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'writeit.writeitinstance': {
            'Meta': {'object_name': 'WriteItInstance', '_ormbases': [u'writeit.WriteItDocument']},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'writeitdocument_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['writeit.WriteItDocument']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['elections']