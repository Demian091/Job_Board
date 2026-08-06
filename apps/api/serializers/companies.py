from rest_framework import serializers
from apps.companies.models import Company

class CompanyListSerializer(serializers.ModelSerializer):
    open_jobs_count = serializers.IntegerField(source='jobs.filter.status', read_only=True)
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'slug', 'industry', 'company_size', 
                  'location', 'logo', 'open_jobs_count', 'is_verified']

class CompanyDetailSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField()
    
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['slug', 'owner', 'created_at']

class CompanyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name', 'description', 'industry', 'company_size',
                  'founded_year', 'website', 'email', 'phone', 'location',
                  'address', 'logo', 'cover_image', 'linkedin', 'twitter', 'facebook']
                  