from rest_framework import serializers
from .models import Resume
import json

class JSONField(serializers.Field):
    def to_representation(self, value):
        # Convert JSON string to Python object for API response
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return []
        return []

    def to_internal_value(self, data):
        # Convert Python object to JSON string for storage
        if data:
            return json.dumps(data)
        return '[]'

class ResumeSerializer(serializers.ModelSerializer):
    education = JSONField(required=False, allow_null=True)
    experience = JSONField(required=False, allow_null=True)
    projects = JSONField(required=False, allow_null=True)

    class Meta:
        model = Resume
        fields = [
            'full_name', 'email', 'phone', 'address', 'linkedin', 'objective',
            'education', 'work_experience', 'skills', 'projects',
            'certifications', 'references'
        ]
        extra_kwargs = {
            'full_name': {'required': False, 'allow_null': True},
            'email': {'required': False, 'allow_null': True},
            'phone': {'required': False, 'allow_null': True},
            'address': {'required': False, 'allow_null': True},
            'linkedin': {'required': False, 'allow_null': True},
            'objective': {'required': False, 'allow_null': True},
            'work_experience': {'required': False, 'allow_null': True},
            'skills': {'required': False, 'allow_null': True},
            'projects': {'required': False, 'allow_null': True},
            'certifications': {'required': False, 'allow_null': True},
            'references': {'required': False, 'allow_null': True},
        }

    def validate(self, data):
        # Ensure JSON fields are lists if provided
        for field in ['education', 'work_experience', 'projects']:
            if field in data and data[field]:
                if not isinstance(data[field], list):
                    raise serializers.ValidationError({field: "Must be a list"})
        return data