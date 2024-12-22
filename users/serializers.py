from rest_framework import serializers
from core.models import ShelterUser

class SignupSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShelterUser
        exclude = ['created_at', 'updated_at']
        extra_kwargs = {'password':{'write_only':True}}
    
    def create(self, validated_data):
        user = ShelterUser.objects.create_user(**validated_data)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)