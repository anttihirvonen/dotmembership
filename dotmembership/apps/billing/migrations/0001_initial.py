# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invoice'
        db.create_table('billing_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invoices', to=orm['members.Member'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='created', max_length=15)),
            ('for_year', self.gf('django.db.models.fields.IntegerField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('due_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('payment_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('payment_method', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('reference_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('billing', ['Invoice'])


    def backwards(self, orm):
        # Deleting model 'Invoice'
        db.delete_table('billing_invoice')


    models = {
        'billing.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'for_year': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoices'", 'to': "orm['members.Member']"}),
            'payment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'payment_method': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'reference_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'created'", 'max_length': '15'})
        },
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

    complete_apps = ['billing']