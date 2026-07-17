from django.contrib import admin
from .models import Customer, Category, Course, News
from django import forms

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
    list_display = ("category", "name", 'kid_age', 'price', 'date_price', 'image', 'description_short', 'description',)
    
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
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 15,
                'cols': 80,
                'style': 'width: 100%; min-height: 300px;'
            }),
            'description_short': forms.Textarea(attrs={'rows': 3}),
        }


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('title', 'published_date', 'is_active')
    list_filter = ('is_active', 'published_date')
    search_fields = ('title', 'description_short', 'content')
    prepopulated_fields = {} # slug генерується автоматично у моделі, якщо порожній
    date_hierarchy = 'published_date'