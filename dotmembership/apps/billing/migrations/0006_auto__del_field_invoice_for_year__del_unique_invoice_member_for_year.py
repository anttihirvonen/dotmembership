# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Invoice', fields ['member', 'for_year']
        db.delete_unique('billing_invoice', ['member_id', 'for_year'])

        # Deleting field 'Invoice.for_year'
        db.delete_column('billing_invoice', 'for_year')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Invoice.for_year'
        raise RuntimeError("Cannot reverse this migration. 'Invoice.for_year' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Invoice.for_year'
        db.add_column('billing_invoice', 'for_year',
                      self.gf('django.db.models.fields.IntegerField')(),
                      keep_default=False)

        # Adding unique constraint on 'Invoice', fields ['member', 'for_year']
        db.create_unique('billing_invoice', ['member_id', 'for_year'])


    models = {
        'billing.annualfee': {
            'Meta': {'object_name': 'AnnualFee'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'year': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'billing.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'fee': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['billing.AnnualFee']", 'null': 'True'}),
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