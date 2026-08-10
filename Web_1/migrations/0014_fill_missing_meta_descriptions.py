from django.db import migrations

# Курси, у яких на момент SEO-аудиту (серпень 2026) було порожнє
# поле meta_description — і, відповідно, порожній <meta name="description">
# на живих проіндексованих сторінках /course/<name_url>/.
META_DESCRIPTIONS = {
    "photoshop": (
        "Курс «Освоєння Photoshop» для дітей від 10 років у школі KODIM "
        "у Первомайську. Обробка фото, колажі, ретуш і основи графічного "
        "дизайну на практичних проєктах. Запишіться на курс!"
    ),
    "computer-basics": (
        "Курс «Комп'ютерна грамотність» для дітей від 6 років у KODIM "
        "(Первомайськ). Основи роботи з ПК, клавіатурою, файлами та "
        "інтернетом — перший крок перед програмуванням. Запишіться!"
    ),
    "javascript-gamedev": (
        "Курс JavaScript для дітей та підлітків від 11 років у школі "
        "KODIM у Первомайську. Створення браузерних і мобільних ігор "
        "з нуля: логіка, анімація, власні проєкти в портфоліо."
    ),
}


# Ті самі 3 курси мали порожнім і description_short — коротший текст,
# що показується безпосередньо під H1 на сторінці курсу
# ({% if course.description_short %}<p class="cd-hero-desc">...{% endif %}).
# Без нього H1 "висить" без жодного тексту — тонкий контент для Google.
DESCRIPTION_SHORT = {
    "photoshop": (
        "Навчаємо дітей від 10 років обробляти фото, створювати колажі "
        "та розуміти основи графічного дизайну в Adobe Photoshop."
    ),
    "computer-basics": (
        "Базовий курс для дітей від 6 років: клавіатура, файли, "
        "інтернет і безпечна робота за комп'ютером."
    ),
    "javascript-gamedev": (
        "Створюємо перші браузерні та мобільні ігри на JavaScript — "
        "від логіки гри до власного проєкту в портфоліо."
    ),
}


def fill_meta_descriptions(apps, schema_editor):
    Course = apps.get_model("Web_1", "Course")
    for name_url, meta_description in META_DESCRIPTIONS.items():
        Course.objects.filter(
            name_url=name_url, meta_description__isnull=True
        ).update(meta_description=meta_description)
        Course.objects.filter(
            name_url=name_url, meta_description=""
        ).update(meta_description=meta_description)

    for name_url, description_short in DESCRIPTION_SHORT.items():
        Course.objects.filter(
            name_url=name_url, description_short__isnull=True
        ).update(description_short=description_short)
        Course.objects.filter(
            name_url=name_url, description_short=""
        ).update(description_short=description_short)


def noop_reverse(apps, schema_editor):
    # Свідомо не відкочуємо контент назад до порожнього значення.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("Web_1", "0013_alter_news_content"),
    ]

    operations = [
        migrations.RunPython(fill_meta_descriptions, noop_reverse),
    ]
