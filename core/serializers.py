from rest_framework import serializers
from .models import *
from rest_framework import status

class ShelterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelterUser
        fields = ['email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if len(data['password']) < 8:
            raise serializers.ValidationError({"password": "must have at least 8 characters"})
        else:
            return data

    def create(self, validated_data):
        user = ShelterUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)


class AnimalOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalOnboarding
        fields = '__all__'


class AnimalHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalHealth
        fields = '__all__'


class PreviousOwnerSerializer(serializers.ModelSerializer):
     class Meta:
        model = PreviousOwnerInfo
        fields = '__all__'


class ShelterAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelterAssessment
        fields = '__all__'


class ShelterAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelterAssessment
        fields = '__all__'


class PotentialAdopterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotentialAdopterInfo
        fields = '__all__'


class HomeInspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeInspectionPreAdoption
        fields = '__all__'


class OutcomePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OutcomePrediction
        fields = '__all__'