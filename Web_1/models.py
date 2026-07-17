from django.utils import timezone 
import os
from io import BytesIO
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.core.files import File
from django.urls import reverse
from PIL import Image

# ── Валідатор розміру файлу ──────────────────────────────────
def validate_image_size(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 5.0  # Максимальний розмір у Мегабайтах
    if filesize > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальний розмір файла — {megabyte_limit} МБ.")


# ── Моделі ───────────────────────────────────────────────────

class Customer(models.Model):
    name = models.CharField(max_length=50, help_text='не більше 20 символів')
    email = models.EmailField()
    phone = models.CharField(max_length=15, help_text='не більше 15 символів')
    message = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'


class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Початківець'),
        ('intermediate', 'Середній'),
        ('advanced', 'Просунутий'),
    ]

    # ── Основне ──────────────────────────────────────────────
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        help_text='оберіть категорію',
        verbose_name='категорія курсу',
        null=True,
    )
    name = models.CharField(max_length=50, verbose_name="Ім'я")
    name_url = models.CharField(
        max_length=50, verbose_name='Name URL', default='', blank=True
    )
    image = models.ImageField(
        upload_to='course_images',
        verbose_name='Картинка',
        null=True,
        blank=True,
        validators=[validate_image_size]  # Додано перевірку ваги файлу
    )
    emoji_icon = models.CharField(
        max_length=10,
        verbose_name='Емодзі іконка',
        default='🎮',
        blank=True,
        help_text='Емодзі, що відображається на картці курсу (напр. 🎮, 🐍, 🎨)',
    )

    # ── Короткий опис і повний опис ──────────────────────────
    description_short = models.CharField(
        max_length=250,
        verbose_name='Короткий опис',
        null=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name='Опис',
        null=True,
        blank=True,
        help_text='Детальний опис курсу (відображається у секції "Як проходить навчання")',
    )

    # ── Параметри курсу ──────────────────────────────────────
    kid_age = models.CharField(
        max_length=50,
        verbose_name='Вік учня',
        null=True,
        blank=True,
        help_text='Напр. «від 10 років» або «8–14 років»',
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        verbose_name='Рівень',
        default='beginner',
    )
    duration = models.CharField(
        max_length=50,
        verbose_name='Тривалість курсу',
        null=True,
        blank=True,
        help_text='Напр. «5 місяців», «3 місяці»',
    )
    lessons_count = models.PositiveSmallIntegerField(
        verbose_name='Кількість занять',
        null=True,
        blank=True,
    )
    schedule = models.CharField(
        max_length=100,
        verbose_name='Розклад',
        null=True,
        blank=True,
        help_text='Напр. «2 заняття на тиждень по 90 хвилин»',
    )

    # ── Ціни ─────────────────────────────────────────────────
    price = models.CharField(
        max_length=50,
        verbose_name='Вартість',
        null=True,
        blank=True,
        help_text='Залишіть порожнім або вкажіть базову ціну для SEO',
    )
    date_price = models.IntegerField(
        verbose_name='Дата_ціна',
        null=True,
        blank=True,
    )
    price_monthly = models.CharField(
        max_length=50,
        verbose_name='Ціна (помісячна)',
        null=True,
        blank=True,
        help_text='Напр. «1200 грн» або «Уточніть»',
    )
    price_semester = models.CharField(
        max_length=50,
        verbose_name='Ціна (семестр)',
        null=True,
        blank=True,
        help_text='Напр. «6500 грн» або «Знижка»',
    )
    price_full = models.CharField(
        max_length=50,
        verbose_name='Ціна (повна)',
        null=True,
        blank=True,
        help_text='Напр. «11000 грн» або «Макс. знижка»',
    )

    # ── Статистика (hero stats bar) ───────────────────────────
    stat_students = models.PositiveIntegerField(
        verbose_name='Учнів пройшло',
        null=True,
        blank=True,
        help_text='Напр. 120',
    )
    stat_projects = models.PositiveIntegerField(
        verbose_name='Проєктів створено',
        null=True,
        blank=True,
    )
    stat_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name='Рейтинг',
        null=True,
        blank=True,
        help_text='Напр. 4.9',
    )
    stat_years = models.PositiveSmallIntegerField(
        verbose_name='Років викладаємо',
        null=True,
        blank=True,
    )

    # ── JSON-секції сторінки ──────────────────────────────────
    what_will_learn = models.JSONField(
        verbose_name='Що вивчить дитина',
        null=True,
        blank=True,
        help_text=(
            'Список рядків. Приклад: '
            '["Основи Lua", "Створення 3D-світів", "Публікація гри"]'
        ),
    )

    for_whom = models.JSONField(
        verbose_name='Для кого курс',
        null=True,
        blank=True,
        help_text=(
            'Список об\'єктів. Приклад: '
            '[{"icon": "🎮", "title": "Фанати Roblox", '
            '"text": "Хочуть не просто грати, а створювати"}]'
        ),
    )

    advantages = models.JSONField(
        verbose_name='Переваги напряму',
        null=True,
        blank=True,
        help_text=(
            'Список нумерованих переваг курсу/професії. Приклад: '
            '[{"title": "Висока затребуваність", '
            '"text": "Python — одна з найпопулярніших мов програмування у світі"}]'
        ),
    )

    program_modules = models.JSONField(
        verbose_name='Програма (модулі)',
        null=True,
        blank=True,
        help_text=(
            'Список модулів. Приклад: '
            '[{"num": "01", "title": "Знайомство з Roblox Studio", '
            '"subtitle": "Інтерфейс та перший світ", '
            '"topics": ["Інтерфейс редактора", "Перша локація"]}]'
        ),
    )

    results = models.JSONField(
        verbose_name='Результати курсу',
        null=True,
        blank=True,
        help_text=(
            'Список результатів. Приклад: '
            '[{"icon": "🏆", "text": "Власна гра у Roblox"}]'
        ),
    )

    faq = models.JSONField(
        verbose_name='Часті запитання (FAQ)',
        null=True,
        blank=True,
        help_text=(
            'Список питань/відповідей. Приклад: '
            '[{"question": "З якого віку?", "answer": "Від 10 років."}]'
        ),
    )

    # ── Мета ─────────────────────────────────────────────────
    meta_description = models.CharField(
        max_length=300,
        verbose_name='Meta опис (SEO)',
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активний',
        help_text='Якщо знято — курс не відображається на сайті',
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='Порядок сортування',
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курси'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course-detail', args=[str(self.id)])

    def get_level_display_ua(self):
        return dict(self.LEVEL_CHOICES).get(self.level, self.level)

    # ── Автоматична конвертація в WebP при збереженні ─────────
    def save(self, *args, **kwargs):
        # Перевіряємо, чи завантажено файл і чи є у нього об'єкт файлу
        if self.image and hasattr(self.image, 'file'):
            img = Image.open(self.image)
            
            # Якщо формат файлу не WEBP, конвертуємо його
            if img.format != 'WEBP':
                img_io = BytesIO()
                
                # Конвертуємо в RGB, якщо зображення в RGBA (з прозорістю, наприклад PNG)
                # WebP підтримує прозорість, але Pillow вимагає збереження режиму
                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGBA', img.size, (255, 255, 255, 0))
                    img = Image.alpha_composite(background, img)
                
                # Зберігаємо у буфер з оптимізацією якості
                img.save(img_io, format='WEBP', quality=85)
                
                # Отримуємо чисте ім'я файлу без старого розширення (.jpg/.png)
                current_name = os.path.splitext(self.image.name)[0]
                new_name = f"{current_name}.webp"
                
                # Записуємо новий сконвертований файл назад у поле image
                # Сягаємо save=False, щоб не викликати рекурсивний save()
                self.image.save(new_name, File(img_io), save=False)
                
        super().save(*args, **kwargs)
def slugify_uk(value):
    """Транслітерація кирилиці в латиницю для ЧПУ (slug), бо slugify()
    сам по собі вирізає кириличні символи і лишає порожній рядок."""
    table = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e',
        'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i',
        'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'shch', 'ь': '', 'ю': 'iu', 'я': 'ia', "'": '',
    }
    value = value.lower()
    value = ''.join(table.get(ch, ch) for ch in value)
    return slugify(value, allow_unicode=False)


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name='URL (slug)',
        help_text='Залиште порожнім — згенерується автоматично з заголовка. '
                   'Використовується у людино-зрозумілому URL новини.',
    )
    image = models.ImageField(
        upload_to='news_images',
        verbose_name='Зображення',
        null=True,
        blank=True,
        validators=[validate_image_size],
    )
    description_short = models.CharField(
        max_length=300,
        verbose_name='Короткий опис',
        help_text='Використовується в анонсі на сторінці "Новини" та як SEO-опис, '
                   'якщо окремий meta-опис не вказано.',
    )
    content = models.TextField(
        verbose_name='Текст новини',
        help_text='Основний текст. Порожні рядки утворюють нові абзаци.',
    )
    published_date = models.DateTimeField(default=timezone.now,
        verbose_name='Дата публікації',
    )

    # ── Мета (SEO) ─────────────────────────────────────────────
    meta_description = models.CharField(
        max_length=300,
        verbose_name='Meta опис (SEO)',
        null=True,
        blank=True,
        help_text='Якщо не вказано — використовується короткий опис.',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна',
        help_text='Якщо знято — новина не відображається на сайті',
    )

    class Meta:
        verbose_name = 'Новина'
        verbose_name_plural = 'Новини'
        ordering = ['-published_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news-detail', args=[self.slug])

    def get_meta_description(self):
        return self.meta_description or self.description_short

    def save(self, *args, **kwargs):
        # Автогенерація slug з заголовка, якщо не задано вручну
        if not self.slug:
            base_slug = slugify_uk(self.title) or 'novyna'
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                counter += 1
                slug = f'{base_slug}-{counter}'
            self.slug = slug

        # Автоконвертація зображення в WebP (як у Web_1.models.Course)
        if self.image and hasattr(self.image, 'file'):
            img = Image.open(self.image)

            if img.format != 'WEBP':
                img_io = BytesIO()

                if img.mode in ('RGBA', 'LA'):
                    background = Image.new('RGBA', img.size, (255, 255, 255, 0))
                    img = Image.alpha_composite(background, img)

                img.save(img_io, format='WEBP', quality=85)

                current_name = os.path.splitext(self.image.name)[0]
                new_name = f'{current_name}.webp'
                self.image.save(new_name, File(img_io), save=False)

        super().save(*args, **kwargs)