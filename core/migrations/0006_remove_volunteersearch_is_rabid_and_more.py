# Generated by Django 5.1 on 2024-08-10 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_volunteersearch_animal_health_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteersearch',
            name='is_rabid',
        ),
        migrations.RemoveField(
            model_name='volunteersearch',
            name='is_visibly_injured',
        ),
        migrations.RemoveField(
            model_name='volunteersearch',
            name='name_of_volunteer',
        ),
        migrations.AddField(
            model_name='animalhealth',
            name='is_injured',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='animalhealth',
            name='is_rabid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='volunteersearch',
            name='animal_health',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.animalhealth'),
        ),
        migrations.AlterField(
            model_name='volunteersearch',
            name='animal_onboarding',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.animalonboarding'),
        ),
    ]