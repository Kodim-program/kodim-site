from django.db import migrations


def link_tests_to_materials(apps, schema_editor):
    Test = apps.get_model('learning', 'Test')
    Material = apps.get_model('learning', 'Material')

    for test in Test.objects.all():
        if test.material_id:
            continue
        if not test.course_id:
            continue

        candidates = Material.objects.filter(course_id=test.course_id)

        # 1) точний збіг назви тесту й назви матеріалу (найчастіший випадок)
        material = candidates.filter(title__iexact=test.title).first()

        # 2) назва тесту міститься в назві матеріалу (або навпаки)
        if not material:
            material = candidates.filter(title__icontains=test.title).first()
        if not material:
            for m in candidates:
                if m.title and m.title.lower() in (test.title or '').lower():
                    material = m
                    break

        # 3) запасний варіант — перший матеріал курсу за порядком
        if not material:
            material = candidates.order_by('order').first()

        if material:
            test.material = material
            test.save(update_fields=['material'])


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0003_test_material_alter_test_course'),
    ]

    operations = [
        migrations.RunPython(link_tests_to_materials, noop_reverse),
    ]
