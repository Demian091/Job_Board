from rest_framework import serializers
from apps.accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type', 
                  'phone', 'location', 'profile_picture', 'bio', 'skills',
                  'experience_years', 'company_name', 'resume']
        read_only_fields = ['id', 'email', 'user_type']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    user_type = serializers.ChoiceField(choices=User.USER_TYPES)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 
                  'user_type', 'company_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            user_type=validated_data['user_type'],
            company_name=validated_data.get('company_name', '')
        )
        return user

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'location', 
                  'profile_picture', 'bio', 'skills', 'experience_years', 'resume']
                  