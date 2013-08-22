# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models


class Migration(DataMigration):
    def forwards(self, orm):
        """
        Links an instance of AnnualFee to all Invoice objects.

        Since 2012 is the only year the membership system has
        been active, we only write out the default 2012
        membership fee data:
            - start date 1.5.2012
            - end date 31.8.2013 (new period begins on 1.9.2013)
            - sum: 5 euros
        """
        # Note: Don't use "from appname.models import ModelName".
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        annual_fee_defaults = {
            'amount': '5.00',
            'start_date': datetime.date(2012, 5, 1),
            'end_date': datetime.date(2013, 8, 31)
        }
        fee = orm.AnnualFee.objects.get_or_create(year=2012, defaults=annual_fee_defaults)[0]

        for invoice in orm.Invoice.objects.all():
            invoice.fee = fee
            invoice.save()

    def backwards(self, orm):
        for invoice in orm.Invoice.objects.all():
            invoice.fee = None
            invoice.save()

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
            'Meta': {'unique_together': "(('member', 'for_year'),)", 'object_name': 'Invoice'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'fee': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['billing.AnnualFee']", 'null': 'True'}),
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
    symmetrical = True
