from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import (
    Material, Enrollment, MaterialProgress,
    Test, Question, Answer, TestResult,
)


# ── Матеріали курсу ────────────────────────────────────────────
class MaterialAdminForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
        widgets = {
            'content': CKEditor5Widget(config_name='news'),
        }


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    form = MaterialAdminForm
    list_display = ('course', 'order', 'title')
    list_filter = ('course',)
    ordering = ('course', 'order')


# ── Призначення курсів учням ───────────────────────────────────
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'assigned_at', 'progress_display')
    list_filter = ('course',)
    search_fields = ('user__username', 'user__email', 'course__name')
    autocomplete_fields = ('user',)

    @admin.display(description='Прогрес')
    def progress_display(self, obj):
        return f'{obj.progress_percent()}% ({obj.read_materials_count()}/{obj.total_materials()})'


@admin.register(MaterialProgress)
class MaterialProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'material', 'is_read', 'read_at')
    list_filter = ('is_read', 'material__course')
    search_fields = ('user__username',)


# ── Тести ───────────────────────────────────────────────────────
class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'order', 'text', 'question_type')
    list_filter = ('test',)
    inlines = [AnswerInline]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'passing_score', 'max_attempts')
    inlines = [QuestionInline]


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'score', 'passed', 'completed_at')
    list_filter = ('test', 'passed')
    search_fields = ('user__username',)
