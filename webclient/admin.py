from webclient.models import *

from django.contrib import admin
from django import forms
from django.db.models import Count
from django.utils.html import mark_safe, format_html
from image_ops.convert_images import SVGString, SVGStringToImageBlob, RenderSVGString
import base64



admin.site.register(Image)
#admin.site.register(ImageLabel)
admin.site.register(ImageSourceType)
admin.site.register(CategoryType)
admin.site.register(ImageFilter)


class ImageLabelInline(admin.TabularInline):
    model = ImageLabel
    fields = ( 'categoryType', 'parentImage', 'imageWindow', 'pub_date')
    readonly_fields = ('parentImage', 'categoryType', 'imageWindow', 'pub_date')
    extra = 0
    show_change_link = True
    can_delete = False
    ordering = ['pub_date']

@admin.register(Labeler)
class LabelerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {'fields': ['user']}),
        #('Image Labels', {'fields': ['ImageLabel_set']})
    ]
    inlines = [ImageLabelInline]


class ImageLabelAdminForm(forms.ModelForm):
    class Meta:
        fields = "__all__"
        model = ImageLabel
        widgets = {
            'overlayed_image': forms.ImageField()
        }

@admin.register(ImageLabel)
class ImageLabelAdmin(admin.ModelAdmin):
    list_display = ('parentImage', 'categoryType', 'imageWindow', 'labeler', 'timeTaken', 'pub_date')
    readonly_fields = ('overlayed_image', )

    def overlayed_image(self, obj):
        print SVGString(obj.labelShapes, keepImage=True)
        blob = RenderSVGString(SVGString(obj.labelShapes, keepImage=True))
        b64 = base64.b64encode(blob)
        return format_html('<img src="data:image/png;base64,{}" alt="Rendered Image Label"></>',
                           b64)
