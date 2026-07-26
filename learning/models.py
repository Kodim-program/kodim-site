from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field

from Web_1.models import Course


# ──────────────────────────────────────────────────────────────
#  Матеріали курсу
# ──────────────────────────────────────────────────────────────
class Material(models.Model):
    """Один розділ/урок курсу. Проходяться СУВОРО по черзі (за полем order)."""

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='materials',
        verbose_name='Курс',
    )
    title = models.CharField('Назва матеріалу', max_length=200)
    order = models.PositiveSmallIntegerField(
        'Порядок', default=0,
        help_text='Визначає послідовність проходження (1, 2, 3 ...).',
    )
    content = CKEditor5Field('Текст матеріалу', config_name='news', blank=True)
    video_url = models.URLField('Посилання на відео (YouTube)', blank=True, null=True)
    file = models.FileField(
        'Файл (PDF тощо)', upload_to='materials/', blank=True, null=True,
    )

    class Meta:
        ordering = ['course', 'order']
        verbose_name = 'Матеріал курсу'
        verbose_name_plural = 'Матеріали курсу'
        unique_together = ('course', 'order')

    def __str__(self):
        return f'{self.course.name} — {self.order}. {self.title}'

    def is_unlocked_for(self, user):
        """Матеріал відкритий, якщо це перший матеріал курсу,
        або попередній матеріал уже прочитано цим учнем."""
        if self.order <= 1:
            return True
        previous = Material.objects.filter(
            course=self.course, order__lt=self.order
        ).order_by('-order').first()
        if previous is None:
            return True
        return MaterialProgress.objects.filter(
            user=user, material=previous, is_read=True
        ).exists()


# ──────────────────────────────────────────────────────────────
#  Призначення курсу учню (робить адмін)
# ──────────────────────────────────────────────────────────────
class Enrollment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='enrollments', verbose_name='Учень',
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='enrollments', verbose_name='Курс',
    )
    assigned_at = models.DateTimeField('Призначено', auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'Призначення курсу'
        verbose_name_plural = 'Призначення курсів'

    def __str__(self):
        return f'{self.user.username} → {self.course.name}'

    # ── Прогрес ────────────────────────────────────────────
    def total_materials(self):
        return self.course.materials.count()

    def read_materials_count(self):
        return MaterialProgress.objects.filter(
            user=self.user, material__course=self.course, is_read=True
        ).count()

    def progress_percent(self):
        total = self.total_materials()
        if total == 0:
            return 0
        return round(self.read_materials_count() / total * 100)

    def all_materials_read(self):
        total = self.total_materials()
        return total > 0 and self.read_materials_count() == total

    def materials_with_status(self):
        """Список матеріалів з позначками read/unlocked — зручно для шаблону."""
        result = []
        for material in self.course.materials.all():
            result.append({
                'material': material,
                'is_read': MaterialProgress.objects.filter(
                    user=self.user, material=material, is_read=True
                ).exists(),
                'is_unlocked': material.is_unlocked_for(self.user),
            })
        return result


class MaterialProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    is_read = models.BooleanField('Прочитано', default=False)
    read_at = models.DateTimeField('Дата прочитання', null=True, blank=True)

    class Meta:
        unique_together = ('user', 'material')
        verbose_name = 'Прогрес по матеріалу'
        verbose_name_plural = 'Прогрес по матеріалах'

    def __str__(self):
        return f'{self.user.username} — {self.material}'


# ──────────────────────────────────────────────────────────────
#  Тестування (тільки варіанти відповідей, авто-перевірка)
# ──────────────────────────────────────────────────────────────
class Test(models.Model):
    course = models.OneToOneField(
        Course, on_delete=models.CASCADE, related_name='test',
        verbose_name='Курс',
    )
    title = models.CharField('Назва тесту', max_length=200, default='Підсумковий тест')
    passing_score = models.PositiveSmallIntegerField(
        'Прохідний бал, %', default=70,
    )
    max_attempts = models.PositiveSmallIntegerField(
        'Максимум спроб', default=3,
    )

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тести'

    def __str__(self):
        return f'{self.course.name} — {self.title}'

    def attempts_used(self, user):
        return TestResult.objects.filter(user=user, test=self).count()

    def attempts_left(self, user):
        return max(self.max_attempts - self.attempts_used(user), 0)

    def best_result(self, user):
        return TestResult.objects.filter(
            user=user, test=self
        ).order_by('-score').first()


class Question(models.Model):
    SINGLE = 'single'
    MULTIPLE = 'multiple'
    TYPE_CHOICES = [
        (SINGLE, 'Одна правильна відповідь'),
        (MULTIPLE, 'Кілька правильних відповідей'),
    ]

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField('Текст питання')
    question_type = models.CharField(
        'Тип питання', max_length=10, choices=TYPE_CHOICES, default=SINGLE,
    )
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Питання'
        verbose_name_plural = 'Питання'

    def __str__(self):
        return self.text[:60]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Варіант відповіді', max_length=300)
    is_correct = models.BooleanField('Правильна відповідь', default=False)

    class Meta:
        verbose_name = 'Варіант відповіді'
        verbose_name_plural = 'Варіанти відповідей'

    def __str__(self):
        return self.text


class TestResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    score = models.PositiveSmallIntegerField('Результат, %')
    passed = models.BooleanField('Складено', default=False)
    completed_at = models.DateTimeField('Дата проходження', auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']
        verbose_name = 'Результат тесту'
        verbose_name_plural = 'Результати тестів'

    def __str__(self):
        return f'{self.user.username} — {self.test} — {self.score}%'
