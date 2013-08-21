# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table('members_member', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('home_town', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('major', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('class_year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('membership_type', self.gf('django.db.models.fields.CharField')(default='normal', max_length=15)),
        ))
        db.send_create_signal('members', ['Member'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table('members_member')


    models = {
        'members.member': {
            'Meta': {'object_name': 'Member'},
            'class_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'home_town': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'membership_type': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '15'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'})
        }
    }

    complete_apps = ['members']