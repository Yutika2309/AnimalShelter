# Generated by Django 5.0.4 on 2024-04-07 04:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnimalOnboarding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_id', models.CharField(editable=False, max_length=12, null=True, unique=True)),
                ('breed', models.CharField(blank=True, max_length=30, null=True)),
                ('age_in_years', models.FloatField()),
                ('colour', models.CharField(blank=True, max_length=30, null=True)),
                ('species', models.CharField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('other', 'Other')], max_length=30)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')], max_length=30)),
                ('weight_in_kgs', models.FloatField()),
                ('distinctive_features', models.CharField(blank=True, max_length=50, null=True)),
                ('micro_chipped', models.BooleanField(default=False)),
                ('cage_id', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('registered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registered_animals', to='core.shelteruser')),
            ],
        ),
        migrations.CreateModel(
            name='AnimalHealth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_status', models.CharField(choices=[('good', 'Good'), ('fair', 'Fair'), ('poor', 'Poor')], max_length=30)),
                ('current_medications', models.CharField(blank=True, max_length=30, null=True)),
                ('known_medical_conditions', models.CharField(blank=True, max_length=30, null=True)),
                ('vaccination_status', models.CharField(choices=[('upto_date', 'Up-to-date'), ('incomplete', 'Incomplete'), ('unknown', 'Unknown')], max_length=30)),
                ('parasite_control', models.CharField(choices=[('flea_tick_prevention', 'Flea-tick-prevention'), ('Deworming', 'deworming')], max_length=30)),
                ('allergies', models.CharField(blank=True, max_length=50, null=True)),
                ('temperament', models.CharField(choices=[('friendly', 'Friendly'), ('shy', 'Shy'), ('aggressive', 'Aggressive')], max_length=30)),
                ('any_aggresive_incidents', models.BooleanField(default=False)),
                ('is_neutered', models.BooleanField(default=False)),
                ('other_observations', models.TextField(blank=True, max_length=200, null=True)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_info', to='core.animalonboarding')),
            ],
        ),
        migrations.CreateModel(
            name='PreviousOwnerInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_owner_known', models.BooleanField(default=True)),
                ('name_of_previous_owner', models.CharField(blank=True, max_length=50, null=True)),
                ('reason_for_intake', models.CharField(choices=[('abandoned', 'Abandoned'), ('owners_moving_away', 'Owner-moving-away'), ('hypoallergens', 'Hypoallergens'), ('unable_to_care_for', 'Unable-to-care-for')], max_length=50)),
                ('los_with_owners_in_years', models.FloatField()),
                ('previous_veterinary_clinic', models.TextField(blank=True, max_length=200, null=True)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='previous_owner_info', to='core.animalonboarding')),
            ],
        ),
        migrations.CreateModel(
            name='ShelterAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cage_id', models.CharField(max_length=20)),
                ('recommended_next_steps', models.CharField(choices=[('medical_evaluation', 'Medical-evaluation'), ('behaviour_analysis', 'Behaviour-analysis')], max_length=100)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shelter_assessments', to='core.animalonboarding')),
            ],
        ),
    ]
