# Generated by Django 5.1 on 2024-08-10 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_rename_lost_animal_health_volunteersearch_animal_health_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteersearch',
            name='animal_health',
            field=models.ForeignKey(choices=[('healthy', 'Healthy'), ('sick', 'Sick'), ('serious', 'Serious')], on_delete=django.db.models.deletion.CASCADE, to='core.animalhealth'),
        ),
        migrations.AlterField(
            model_name='volunteersearch',
            name='animal_onboarding',
            field=models.ForeignKey(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('other', 'Other')], on_delete=django.db.models.deletion.CASCADE, to='core.animalonboarding'),
        ),
    ]
