# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('MomohaFeed_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1024, db_index=True)),
            ('last_poll', self.gf('django.db.models.fields.BigIntegerField')(null=True, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('last_detail_update', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
        ))
        db.send_create_signal('MomohaFeed', ['Feed'])

        # Adding model 'Item'
        db.create_table('MomohaFeed_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MomohaFeed.Feed'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('last_poll', self.gf('django.db.models.fields.BigIntegerField')(null=True, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('published', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('updated', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=65536, null=True)),
            ('last_detail_update', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
        ))
        db.send_create_signal('MomohaFeed', ['Item'])

        # Adding model 'Subscription'
        db.create_table('MomohaFeed_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MomohaFeed.Feed'])),
            ('start', self.gf('django.db.models.fields.BigIntegerField')()),
            ('enable', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('MomohaFeed', ['Subscription'])

        # Adding model 'ItemRead'
        db.create_table('MomohaFeed_itemread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MomohaFeed.Subscription'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MomohaFeed.Item'])),
            ('time', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('enable', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('MomohaFeed', ['ItemRead'])

        # Adding model 'ItemStar'
        db.create_table('MomohaFeed_itemstar', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscription', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MomohaFeed.Subscription'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['MomohaFeed.Item'])),
            ('time', self.gf('django.db.models.fields.BigIntegerField')(db_index=True)),
            ('enable', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('MomohaFeed', ['ItemStar'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table('MomohaFeed_feed')

        # Deleting model 'Item'
        db.delete_table('MomohaFeed_item')

        # Deleting model 'Subscription'
        db.delete_table('MomohaFeed_subscription')

        # Deleting model 'ItemRead'
        db.delete_table('MomohaFeed_itemread')

        # Deleting model 'ItemStar'
        db.delete_table('MomohaFeed_itemstar')


    models = {
        'MomohaFeed.feed': {
            'Meta': {'object_name': 'Feed'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_detail_update': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'last_poll': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'})
        },
        'MomohaFeed.item': {
            'Meta': {'object_name': 'Item'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '65536', 'null': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MomohaFeed.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'last_detail_update': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'last_poll': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'published': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'updated': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'})
        },
        'MomohaFeed.itemread': {
            'Meta': {'object_name': 'ItemRead'},
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MomohaFeed.Item']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MomohaFeed.Subscription']"}),
            'time': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        },
        'MomohaFeed.itemstar': {
            'Meta': {'object_name': 'ItemStar'},
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MomohaFeed.Item']"}),
            'subscription': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MomohaFeed.Subscription']"}),
            'time': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
        },
        'MomohaFeed.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'enable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['MomohaFeed.Feed']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.BigIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['MomohaFeed']