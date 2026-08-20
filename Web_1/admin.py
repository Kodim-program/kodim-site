from django.contrib import admin
from django.utils.html import format_html
from .models import Customer, Category, Course, News, GalleryImage
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    ...

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

#@admin.register(Age)
#class AgeAdmin(admin.ModelAdmin):
#    ...
class CourseAdminForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 15,
                'cols': 80,
                'style': 'width: 100%; min-height: 300px;'
            }),
        }


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ("category", "name", "order", 'kid_age', 'price', 'date_price', 'image', 'description_short', 'description',)
    
    @admin.display()
    def category(self, obj):
        return obj
    category.short_description = 'Name'

#@admin.register(Price)
#class PriceAdmin(admin.ModelAdmin):
#    ...
class NewsAdminForm(forms.ModelForm):

    class Meta:
        model = News
        fields = "__all__"

        widgets = {
            "content": CKEditor5Widget(
                config_name="news"
            ),
            "description_short": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),
        }


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('title', 'published_date', 'is_active')
    list_filter = ('is_active', 'published_date')
    search_fields = ('title', 'description_short', 'content')
    prepopulated_fields = {} # slug генерується автоматично у моделі, якщо порожній
    date_hierarchy = 'published_date'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_preview', 'alt_text', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('alt_text',)
    ordering = ('order', '-created_at')

    @admin.display(description='Прев\'ю')
    def thumbnail_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:60px;width:auto;border-radius:6px;" />',
                obj.image.url,
            )
        return '—'