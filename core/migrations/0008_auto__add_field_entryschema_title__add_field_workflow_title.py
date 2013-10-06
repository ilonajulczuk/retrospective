# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EntrySchema.title'
        db.add_column(u'core_entryschema', 'title',
                      self.gf('django.db.models.fields.CharField')(default='noname', max_length=80),
                      keep_default=False)

        # Adding field 'Workflow.title'
        db.add_column(u'core_workflow', 'title',
                      self.gf('django.db.models.fields.CharField')(default='noname', max_length=80),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EntrySchema.title'
        db.delete_column(u'core_entryschema', 'title')

        # Deleting field 'Workflow.title'
        db.delete_column(u'core_workflow', 'title')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.entry': {
            'Meta': {'object_name': 'Entry'},
            'data': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.EntrySchema']"})
        },
        u'core.entryschema': {
            'Meta': {'object_name': 'EntrySchema'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'fields': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'noname'", 'max_length': '80'}),
            'workflows': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'entryschemas'", 'symmetrical': 'False', 'to': u"orm['core.Workflow']"})
        },
        u'core.failedentry': {
            'Meta': {'object_name': 'FailedEntry', '_ormbases': [u'core.OutputEntry']},
            u'outputentry_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.OutputEntry']", 'unique': 'True', 'primary_key': 'True'}),
            'retrospective': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Retrospective']", 'null': 'True'})
        },
        u'core.learnedentry': {
            'Meta': {'object_name': 'LearnedEntry'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'future_usages': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'goal': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'previous_usage': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'retrospective': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Retrospective']", 'null': 'True'}),
            'skill': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'core.outputentry': {
            'Meta': {'object_name': 'OutputEntry'},
            'goal': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'problems': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']", 'null': 'True'})
        },
        u'core.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'core.retrospective': {
            'Meta': {'object_name': 'Retrospective'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'direction': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'core.successentry': {
            'Meta': {'object_name': 'SuccessEntry', '_ormbases': [u'core.OutputEntry']},
            u'outputentry_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.OutputEntry']", 'unique': 'True', 'primary_key': 'True'}),
            'retrospective': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Retrospective']", 'null': 'True'})
        },
        u'core.workflow': {
            'Meta': {'object_name': 'Workflow'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'entries_metadata': ('jsonfield.fields.JSONField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'noname'", 'max_length': '80'})
        }
    }

    complete_apps = ['core']