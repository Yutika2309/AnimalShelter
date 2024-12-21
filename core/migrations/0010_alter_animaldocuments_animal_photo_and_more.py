# Generated by Django 5.1.4 on 2024-12-21 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_animalonboarding_animal_photo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animaldocuments',
            name='animal_photo',
            field=models.FileField(default=None, null=True, upload_to='animal_image/'),
        ),
        migrations.AlterField(
            model_name='animaldocuments',
            name='other_documents',
            field=models.FileField(default=None, null=True, upload_to='animal_documents/'),
        ),
    ]
