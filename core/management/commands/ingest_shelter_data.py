from django.core.management.base import BaseCommand, CommandError
from core.models import *
import pandas as pd


class Command(BaseCommand):
    help = "Ingesting base data to get going"

    def handle(self, *args, **options):
        df = pd.read_csv('/app/data/animal_onboarding_ingestion.csv')

        index = 0
        for index, row in df.iterrows():

            ao_obj = AnimalOnboarding.objects.create(
                    breed = row['parent_breed'],
                    intake_type = row['intake_type'].lower().replace(' ', '_'),
                    age_in_years = row['age_upon_intake_(years)'],
                    month_of_intake = row['intake_month'],
                    colour = row['color_combination'],
                    species = row['animal_type'],
                    gender = row['sex_of_animal'].lower(),
                    is_mix = True if row['is_mix'] == 'Yes' else False,
                    registered_by = ShelterUser.objects.get(id=1)
                )

            ao_obj.save()

            ah_obj = AnimalHealth.objects.create(
                    animal = ao_obj,
                    intake_condition = row['intake_condition'],
                    neutering_status = row['neutering_status'].lower(),
                )

            ah_obj.save()

            self.stdout.write(
                self.style.SUCCESS(f'DATA INGESTED FOR ANIMAL NO. {index+1}')
            )