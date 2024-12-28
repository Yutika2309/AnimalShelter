from rest_framework import serializers
from core.models import AnimalOnboarding, AnimalHealth, AnimalDocuments

class AnimalOnboardingSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnimalOnboarding
        fields = '__all__'

    def validate_age_in_years(self, value):
        if value < 0:
            raise serializers.ValidationError('The age must be greater than 0.')
        return value