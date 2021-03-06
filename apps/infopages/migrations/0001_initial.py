# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'InfoPage'
        db.create_table('infopages_infopage', (
            ('title_de', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('page_title', self.gf('django.db.models.fields.CharField')(max_length=120, blank=True)),
            ('left_column_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('right_column_pl', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('page_title_en', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('page_title_es', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('left_column_lt', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title_fr', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('right_column_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('left_column_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=120, blank=True)),
            ('title_lt', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('right_column', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('right_column_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('right_column_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('left_column_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title_uk', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('right_column_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('left_column', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('right_column_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('left_column_pl', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('left_column_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('right_column_lt', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title_es', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('page_title_fr', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('page_title_uk', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('page_title_de', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=120, db_index=True)),
            ('page_title_lt', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('right_column_de', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('page_title_pl', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('left_column_es', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('left_column_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('title_pl', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
            ('page_title_ru', self.gf('django.db.models.fields.CharField')(max_length=120, null=True, blank=True)),
        ))

        if not db.dry_run:
            from django.core.management import call_command
            call_command("loaddata", "wl_data")

        db.send_create_signal('infopages', ['InfoPage'])


    def backwards(self, orm):

        # Deleting model 'InfoPage'
        db.delete_table('infopages_infopage')


    models = {
        'infopages.infopage': {
            'Meta': {'object_name': 'InfoPage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_column': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'left_column_de': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'left_column_en': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'left_column_es': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'left_column_fr': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'left_column_lt': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'left_column_pl': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'left_column_ru': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'left_column_uk': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'page_title_de': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'page_title_en': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'page_title_es': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'page_title_fr': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'page_title_lt': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'page_title_pl': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'page_title_ru': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'page_title_uk': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'right_column': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'right_column_de': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'right_column_en': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'right_column_es': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'right_column_fr': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'right_column_lt': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'right_column_pl': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'right_column_ru': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'right_column_uk': ('django.db.models.fields.TextField', [], {'null': True, 'blank': True}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '120', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'title_es': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'title_fr': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'title_lt': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'title_pl': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'title_ru': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True}),
            'title_uk': ('django.db.models.fields.CharField', [], {'max_length': '120', 'null': True, 'blank': True})
        }
    }

    complete_apps = ['infopages']
