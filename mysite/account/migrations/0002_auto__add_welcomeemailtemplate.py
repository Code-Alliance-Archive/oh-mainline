# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'WelcomeEmailTemplate'
        db.create_table('account_welcomeemailtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('referring_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=2048, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=998)),
            ('body', self.gf('tinymce.models.HTMLField')()),
        ))
        db.send_create_signal('account', ['WelcomeEmailTemplate'])


    def backwards(self, orm):
        
        # Deleting model 'WelcomeEmailTemplate'
        db.delete_table('account_welcomeemailtemplate')


    models = {
        'account.invitationrequest': {
            'Meta': {'object_name': 'InvitationRequest'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'account.welcomeemailtemplate': {
            'Meta': {'object_name': 'WelcomeEmailTemplate'},
            'body': ('tinymce.models.HTMLField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'referring_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '998'})
        }
    }

    complete_apps = ['account']
