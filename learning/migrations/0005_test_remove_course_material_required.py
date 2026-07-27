from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0004_link_tests_to_materials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='course',
        ),
        migrations.AlterField(
            model_name='test',
            name='material',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='test',
                to='learning.material',
                verbose_name='Матеріал (урок)',
            ),
        ),
    ]
