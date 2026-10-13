from django.db import models
from django.urls import reverse


# ---------- Спільне ----------
class Technology(models.Model):
    KIND_CHOICES = [
        ("service", "Технологія розробки"),
        ("material", "Матеріал друку"),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)

    class Meta:
        verbose_name = "Технологія / матеріал"
        verbose_name_plural = "Технології / матеріали"

    def __str__(self):
        return f"{self.name} ({self.get_kind_display()})"


# ---------- Розділ «Моделі» ----------
class ModelCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категорія моделей"
        verbose_name_plural = "Категорії моделей"

    def __str__(self):
        return self.name


class Model3D(models.Model):
    SOURCE_CHOICES = [
        ("own", "Власна модель"),
        ("makerworld", "MakerWorld (за посиланням)"),
    ]
    LICENSE_CHOICES = [
        ("own", "Власні права — можна продавати файл і друк"),
        ("commercial_verified", "MakerWorld: комерційна ліцензія підтверджена — можна продавати лише друк"),
        ("noncommercial", "MakerWorld: некомерційна — показ без продажу"),
        ("unknown", "Не перевірено — НЕ показувати кнопку продажу"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        ModelCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="models"
    )
    description = models.TextField(blank=True)

    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="own")
    source_url = models.URLField(blank=True, help_text="Посилання на оригінал на MakerWorld")
    author_name = models.CharField(max_length=150, blank=True, help_text="Автор моделі на MakerWorld")
    license_type = models.CharField(max_length=30, choices=LICENSE_CHOICES, default="unknown")

    thumbnail = models.ImageField(upload_to="models/thumbnails/", blank=True, null=True)
    # Для власних моделей — реальний файл; для MakerWorld це поле НЕ заповнюється
    file = models.FileField(upload_to="models/files/", blank=True, null=True)

    material = models.ForeignKey(
        Technology, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={"kind": "material"}, related_name="models3d",
    )
    delivery_days = models.PositiveIntegerField(null=True, blank=True, help_text="Строк друку, днів")

    print_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True, help_text="Вартість друку на замовлення"
    )
    file_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="Вартість файлу (тільки для source_type='own')",
    )

    is_active = models.BooleanField(default=False, help_text="Показувати на сайті")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "3D-модель"
        verbose_name_plural = "3D-моделі"
        ordering = ["-created_at"]

    def can_sell_print(self):
        return self.license_type in ("own", "commercial_verified")

    def can_sell_file(self):
        return self.license_type == "own" and bool(self.file)

    def get_absolute_url(self):
        return reverse("shop:model_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class OrderRequest(models.Model):
    model3d = models.ForeignKey(Model3D, on_delete=models.CASCADE, related_name="orders")
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    comment = models.TextField(blank=True, help_text="Колір, розмір, кількість тощо")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка на замовлення"
        verbose_name_plural = "Заявки на замовлення"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.model3d.title}"


# ---------- Розділ «Послуги» ----------
class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Категорія послуг"
        verbose_name_plural = "Категорії послуг"

    def __str__(self):
        return self.name


class Service(models.Model):
    KIND_CHOICES = [
        ("app", "Розробка додатків"),
        ("modeling", "3D-моделювання"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    category = models.ForeignKey(
        ServiceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="services"
    )
    technologies = models.ManyToManyField(
        Technology, blank=True, limit_choices_to={"kind": "service"}, related_name="services"
    )
    short_description = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="services/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Послуга"
        verbose_name_plural = "Послуги"

    def get_absolute_url(self):
        return reverse("shop:service_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class ServicePackage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="packages")
    name = models.CharField(max_length=100, help_text="Наприклад: Базовий / Стандарт / Преміум")
    price = models.DecimalField(max_digits=9, decimal_places=2)
    delivery_days = models.PositiveIntegerField(help_text="Строк виконання, днів")
    features = models.TextField(blank=True, help_text="Що входить — кожен пункт з нового рядка")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "price"]
        verbose_name = "Пакет послуги"
        verbose_name_plural = "Пакети послуг"

    @property
    def features_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]

    def __str__(self):
        return f"{self.service.title} — {self.name}"


class ServiceOrder(models.Model):
    package = models.ForeignKey(ServicePackage, on_delete=models.CASCADE, related_name="orders")
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка на послугу"
        verbose_name_plural = "Заявки на послуги"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.package}"