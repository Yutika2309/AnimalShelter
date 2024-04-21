from rest_framework import serializers
from .models import *

class ShelterUserSerializer(serializers.ModelSerializer):
    """
        description: Serializer for the Animal Shelter User
        created by: @Yutika Rege
        date: 21st April 2024
    """
    class Meta:
        model = ShelterUser
        fields = '__all__'


class AnimalOnboardingSerializer(serializers.ModelSerializer):
    """
        description: Serializer for the Animal onboarding
        created by: @Yutika Rege
        date: 21st April 2024
    """
    class Meta:
        model = AnimalOnboarding
        fields = '__all__'


class AnimalHealthSerializer(serializers.ModelSerializer):
    """
        description: Serializer for the Animal Health
        created by: @Yutika Rege
        date: 21st April 2024
    """
    class Meta:
        model = AnimalHealth
        fields = '__all__'


class PreviousOwnerSerializer(serializers.ModelSerializer):
    """
        description: Serializer for the Previous owner information
        created by: @Yutika Rege
        date: 21st April 2024
    """
    class Meta:
        model = PreviousOwnerInfo
        fields = '__all__'


class ShelterAssessmentSerializer(serializers.ModelSerializer):
    """
        description: Serializer for the Shelter assessment
        created by: @Yutika Rege
        date: 21st April 2024
    """
    class Meta:
        model = ShelterAssessment
        fields = '__all__'


class ShelterAssessmentSerializer(serializers.ModelSerializer):
    """
        description: Serializer for the Shelter assessment
        created by: @Yutika Rege
        date: 21st April 2024
    """
    class Meta:
        model = ShelterAssessment
        fields = '__all__'


class PotentialAdopterInfoSerializer(serializers.ModelSerializer):
    """
        description: Serializer for the Potential adopter
        created by: @Yutika Rege
        date: 21st April 2024
    """
    class Meta:
        model = PotentialAdopterInfo
        fields = '__all__'


class HomeInspectionSerializer(serializers.ModelSerializer):
    """
        description: Serializer for the Home inspection
        created by: @Yutika Rege
        date: 21st April 2024
    """
    class Meta:
        model = HomeInspectionPreAdoption
        fields = '__all__'