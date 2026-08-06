from rest_framework import serializers
from apps.jobs.models import Job
from apps.api.serializers.companies import CompanyListSerializer

class JobListSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(read_only=True)
    is_remote = serializers.BooleanField()
    
    class Meta:
        model = Job
        fields = ['id', 'title', 'slug', 'company', 'job_type', 
                  'experience_level', 'location', 'is_remote',
                  'salary_min', 'salary_max', 'created_at', 'is_featured']

class JobDetailSerializer(serializers.ModelSerializer):
    company = CompanyListSerializer(read_only=True)
    posted_by = serializers.StringRelatedField()
    has_applied = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['slug', 'posted_by', 'views_count', 'applications_count']
    
    def get_has_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.applications.filter(applicant=request.user).exists()
        return False

class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'responsibilities',
                  'benefits', 'job_type', 'experience_level', 'salary_min',
                  'salary_max', 'salary_currency', 'location', 'is_remote',
                  'expires_at']
                  