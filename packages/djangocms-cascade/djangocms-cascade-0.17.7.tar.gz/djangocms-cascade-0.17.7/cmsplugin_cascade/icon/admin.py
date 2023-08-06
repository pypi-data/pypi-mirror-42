# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, io, json, shutil
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import ModelForm
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _

from cmsplugin_cascade.models import IconFont
from cmsplugin_cascade import app_settings

import tempfile
try:
    import czipfile as zipfile
except ImportError:
    import zipfile


class UploadIconsForms(ModelForm):
    class Meta:
        fields = ('identifier', 'zip_file')

    @property
    def media(self):
        media = super(UploadIconsForms, self).media
        try:
            css_url = self.instance.get_stylesheet_url()
            media.add_css({'all': ('cascade/css/admin/iconfont.css', css_url,)})
        except AttributeError:
            pass
        return media

    def unzip_archive(self, zip_ref):
        common_prefix = os.path.commonprefix(zip_ref.namelist())
        if not common_prefix:
            raise ValidationError(_("The uploaded zip archive is not packed correctly"))
        icon_font_root = app_settings.CMSPLUGIN_CASCADE['icon_font_root']
        try:
            try:
                os.makedirs(icon_font_root)
            except os.error:
                pass  # the directory exists already
            temp_folder = tempfile.mkdtemp(prefix='', dir=icon_font_root)
            for member in zip_ref.infolist():
                zip_ref.extract(member, temp_folder)
            font_folder = os.path.join(temp_folder, common_prefix)

            # this is specific to fontello
            fh = io.open(os.path.join(font_folder, 'config.json'), 'r')
            config_data = json.load(fh)
        except Exception as e:
            shutil.rmtree(temp_folder, ignore_errors=True)
            raise ValidationError(_("Can not unzip uploaded archive. Reason: {}").__format__(e))
        return os.path.relpath(font_folder, icon_font_root), config_data

    def clean(self):
        cleaned_data = super(UploadIconsForms, self).clean()
        if 'zip_file' in self.changed_data:
            try:
                zip_ref = zipfile.ZipFile(cleaned_data['zip_file'].file.file, 'r')
                cleaned_data.update(zip(['font_folder', 'config_data'], self.unzip_archive(zip_ref)))
            finally:
                zip_ref.close()
        return cleaned_data


@admin.register(IconFont)
class IconFontAdmin(admin.ModelAdmin):
    form = UploadIconsForms

    def save_model(self, request, obj, form, change):
        if 'font_folder' in form.cleaned_data and 'config_data' in form.cleaned_data:
            obj.font_folder = form.cleaned_data['font_folder']
            obj.config_data = form.cleaned_data['config_data']
        super(IconFontAdmin, self).save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(IconFontAdmin, self).get_readonly_fields(request, obj=obj))
        if obj:
            readonly_fields.append('preview_icons')
        return readonly_fields

    def preview_icons(self, obj):
        families = obj.get_icon_families()
        format_string = '<li title="{{0}}"><i class="{css_prefix_text}{{0}}"></i></li>'.format(**obj.config_data)
        return format_html('<div class="preview-iconfont">{}</div>',
            format_html_join('\n', '<h2>{}</h2><ul>{}</ul>',
                 ((src.title(), format_html_join('', format_string, ((g,) for g in glyphs)))
                 for src, glyphs in families.items())))
    preview_icons.short_description = _("Preview Icons")
