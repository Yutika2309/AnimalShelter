# Generated by Django 5.1.4 on 2024-12-21 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_animaldocuments_animal_photo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animalonboarding',
            name='cage_id',
        ),
        migrations.AlterField(
            model_name='animalhealth',
            name='health_status',
            field=models.CharField(choices=[('normal', 'Normal'), ('injured', 'Injured'), ('aged', 'Aged'), ('sick', 'Sick'), ('feral', 'Feral'), ('pregnant', 'Pregnant'), ('nursing', 'Nursing')], max_length=30),
        ),
    ]
