# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-11 14:45
from __future__ import unicode_literals

import colorfield.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djangocms_attributes_field.fields
import djangocms_link.validators
import djangocms_text_ckeditor.fields
import filer.fields.image
import stackable_plugins.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('cms', '0020_old_tree_cleanup'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiographyPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='stackable_plugins_biographyplugin', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('renderer', models.CharField(blank=True, choices=[('renderers_by_class/rendered_biography/default.html', 'DEFAULT: Biography')], default='renderers_by_class/rendered_biography/default.html', max_length=200, null=True, verbose_name='Renderer')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('byline', models.CharField(blank=True, max_length=200, null=True, verbose_name='Byline')),
                ('text_block', djangocms_text_ckeditor.fields.HTMLField()),
                ('headshot', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CompareTwoThingsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='stackable_plugins_comparetwothingsplugin', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('renderer', models.CharField(blank=True, choices=[('renderers_by_class/rendered_comparison/default.html', 'DEFAULT: Side by Side Comparison - Image above Text block')], default='renderers_by_class/rendered_comparison/default.html', max_length=200, null=True, verbose_name='Renderer')),
                ('title_left', models.CharField(max_length=200, verbose_name='Left Title')),
                ('body_left', djangocms_text_ckeditor.fields.HTMLField()),
                ('conjunction', models.CharField(blank=True, choices=[('and', 'And'), ('or', 'Or'), ('versus', 'Vs.')], max_length=10, null=True, verbose_name='Comparison Conjuction')),
                ('title_right', models.CharField(max_length=200, verbose_name='Right Title')),
                ('body_right', djangocms_text_ckeditor.fields.HTMLField()),
                ('image_left', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, related_name='left_image', to=settings.FILER_IMAGE_MODEL)),
                ('image_right', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, related_name='right_image', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CountdownClockPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='stackable_plugins_countdownclockplugin', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('renderer', models.CharField(blank=True, choices=[('renderers_by_class/rendered_countdown/default.html', 'DEFAULT: Countdown Clock')], default='renderers_by_class/rendered_countdown/default.html', max_length=200, null=True, verbose_name='Renderer')),
                ('zero_date_time', models.DateTimeField(verbose_name='Zero')),
                ('label', models.CharField(blank=True, help_text="This is a label that appears with the clock, e.g., 'Series Premiere in...'", max_length=400, null=True, verbose_name='Label')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='GenericButtonPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='stackable_plugins_genericbuttonplugin', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('style_attributes', djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, verbose_name='Style Attributes')),
                ('renderer', models.CharField(blank=True, choices=[('renderers_by_class/rendered_button/default.html', 'DEFAULT: Generic Button - a container for children plugins'), ('renderers_by_class/rendered_button/special_button.html', 'This is a special button')], max_length=200, null=True, verbose_name='Renderer')),
                ('external_link', models.URLField(blank=True, help_text='Provide a valid URL to an external website.', max_length=2040, validators=[djangocms_link.validators.IntranetURLValidator(intranet_host_re=None)], verbose_name='External link')),
                ('target', models.CharField(blank=True, choices=[('_blank', 'Open in new window'), ('_self', 'Open in same window')], max_length=255, verbose_name='Target')),
                ('uploaded_file', models.FileField(blank=True, help_text='e.g., a PDF', max_length=255, upload_to='uploaded_files/', verbose_name='File')),
                ('css_class', models.CharField(blank=True, help_text='Apply your own custom CSS class to this button', max_length=255, null=True, verbose_name='CSS Class')),
                ('internal_link', models.ForeignKey(blank=True, help_text='If provided, overrides the external link.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.Page', verbose_name='Internal link')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
        migrations.CreateModel(
            name='GenericContainerPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='stackable_plugins_genericcontainerplugin', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('renderer', models.CharField(blank=True, choices=[('renderers_by_class/rendered_generic/default_generic_container.html', 'DEFAULT: Generic Parent - a container for children plugins'), ('renderers_by_class/rendered_generic/accordion_container.html', 'Accordion: Used to hide/show plugin content on click')], max_length=200, null=True, verbose_name='Renderer')),
                ('alignment', models.CharField(blank=True, choices=[('left', 'Content Floats Left'), ('right', 'Content Floats Right'), ('center-block', 'Content breaks text, centered as its own block')], help_text='Note: child plugins might also re-align their content', max_length=40, null=True, verbose_name='Content Alignment')),
                ('background_color', colorfield.fields.ColorField(blank=True, max_length=18, null=True)),
                ('background_image', filer.fields.image.FilerImageField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='background_image', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='GenericListPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='stackable_plugins_genericlistplugin', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('renderer', models.CharField(blank=True, choices=[('renderers_by_class/rendered_list/default.html', 'DEFAULT: one item per row'), ('renderers_by_class/rendered_list/2_up.html', 'Two items per row'), ('renderers_by_class/rendered_list/3_up.html', 'Three items per row'), ('renderers_by_class/rendered_list/bulleted_list.html', 'Bulleted list of items (links only)'), ('renderers_by_class/rendered_list/carousel.html', 'Items displayed in a carousel')], max_length=200, null=True, verbose_name='Renderer')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='GenericSeparatorPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='stackable_plugins_genericseparatorplugin', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('style_attributes', djangocms_attributes_field.fields.AttributesField(blank=True, default=dict, verbose_name='Style Attributes')),
                ('renderer', models.CharField(blank=True, choices=[('renderers_by_class/rendered_separator/default_generic_separator.html', 'DEFAULT: Generic Separator - a horizontal rule'), ('renderers_by_class/rendered_separator/image_separator.html', 'A centered image - can be icon or a banner')], max_length=200, null=True, verbose_name='Renderer')),
                ('separator_image', filer.fields.image.FilerImageField(blank=True, help_text='If you want an image to be used, add it here (can be an icon or a banner)', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='separator_image', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin', models.Model),
        ),
        migrations.CreateModel(
            name='HostedVideoPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='stackable_plugins_hostedvideoplugin', serialize=False, to='cms.CMSPlugin')),
                ('renderer', models.CharField(blank=True, choices=[('renderers_by_class/hosted_video/default.html', 'DEFAULT: COVE video')], default='renderers_by_class/hosted_video/default.html', max_length=200, null=True, verbose_name='Renderer')),
                ('id_on_service', models.CharField(help_text='For PBS COVE, enter the COVE ID here.', max_length=200, verbose_name='ID on Service')),
                ('duration', models.DurationField(blank=True, default=datetime.timedelta(0), help_text='[DD] [HH:[MM:]]ss[.uuuuuu]', null=True, verbose_name='Duration')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Video Caption')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='HostService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('slug', models.SlugField(max_length=120, unique=True)),
                ('available', models.BooleanField(default=True, verbose_name='Available')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
            ],
            options={
                'verbose_name': 'Video Hosting Service',
                'verbose_name_plural': 'Video Hosting Services',
            },
        ),
        migrations.CreateModel(
            name='ImageWithThumbnailPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='stackable_plugins_imagewiththumbnailplugin', serialize=False, to='cms.CMSPlugin')),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='Title')),
                ('renderer', models.CharField(blank=True, choices=[('renderers_by_class/rendered_image/default.html', 'DEFAULT: Thumbnail clickable to show main image')], default='renderers_by_class/rendered_image/default.html', max_length=200, null=True, verbose_name='Renderer')),
                ('main_image', models.ImageField(blank=True, height_field='main_image_height', help_text='Upload full-sized image.', null=True, upload_to=stackable_plugins.models.get_upload_to, verbose_name='Primary Image', width_field='main_image_width')),
                ('main_image_height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image Height')),
                ('main_image_width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Image Width')),
                ('thumbnail', models.ImageField(blank=True, height_field='thumbnail_height', null=True, upload_to=stackable_plugins.models.get_upload_to, verbose_name='Thumbnail Image', width_field='thumbnail_width')),
                ('thumbnail_height', models.PositiveIntegerField(blank=True, default=64, null=True, verbose_name='Thumbnail Height')),
                ('thumbnail_width', models.PositiveIntegerField(blank=True, default=64, null=True, verbose_name='Image Width')),
                ('caption', djangocms_text_ckeditor.fields.HTMLField()),
                ('credit', models.CharField(blank=True, max_length=255, null=True, verbose_name='Image Credit')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='hostedvideoplugin',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stackable_plugins.HostService'),
        ),
    ]
