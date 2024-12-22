# Generated by Django 5.1.4 on 2024-12-22 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_animalonboarding_breed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelteruser',
            name='usertype',
            field=models.CharField(choices=[('admin', 'Admin'), ('shelterstaff', 'Shelter_staff'), ('adopter_or_foster', 'Adopter_or_foster_parent'), ('volunteer', 'Volunteer')], default='admin', max_length=50),
        ),
    ]