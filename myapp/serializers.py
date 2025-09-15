# serializers.py
from rest_framework import serializers
from .models import Resume
import json

class JSONField(serializers.Field):
    def to_representation(self, value):
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return []
        return []

    def to_internal_value(self, data):
        if data is None:
            return None
        if isinstance(data, str):
            # If it's already a string, assume it's JSON
            try:
                parsed = json.loads(data)  # Validate it's proper JSON
                if isinstance(parsed, list):
                    return data  # Return the JSON string as-is
                else:
                    raise serializers.ValidationError("JSON must represent a list")
            except json.JSONDecodeError:
                raise serializers.ValidationError("Invalid JSON string")
        elif isinstance(data, list):
            return json.dumps(data)  # Convert list to JSON string for storage
        else:
            raise serializers.ValidationError("Must be a list or JSON string")

class ResumeSerializer(serializers.ModelSerializer):
    education = JSONField(required=False, allow_null=True)
    experience = JSONField(required=False, allow_null=True)
    projects = JSONField(required=False, allow_null=True)

    class Meta:
        model = Resume
        fields = [
            'full_name', 'title', 'email', 'phone', 'address', 'location',
            'linkedin', 'github', 'portfolio', 'objective', 'education',
            'experience', 'skills', 'projects', 'languages', 'certifications',
            'awards', 'organizations', 'coCurricular', 'declarations'
        ]
        extra_kwargs = {
            'full_name': {'required': False, 'allow_null': True},
            'title': {'required': False, 'allow_null': True},
            'email': {'required': False, 'allow_null': True},
            'phone': {'required': False, 'allow_null': True},
            'address': {'required': False, 'allow_null': True},
            'location': {'required': False, 'allow_null': True},
            'linkedin': {'required': False, 'allow_null': True},
            'github': {'required': False, 'allow_null': True},
            'portfolio': {'required': False, 'allow_null': True},
            'objective': {'required': False, 'allow_null': True},
            'education': {'required': False, 'allow_null': True},
            'experience': {'required': False, 'allow_null': True},
            'skills': {'required': False, 'allow_null': True},
            'projects': {'required': False, 'allow_null': True},
            'languages': {'required': False, 'allow_null': True},
            'certifications': {'required': False, 'allow_null': True},
            'awards': {'required': False, 'allow_null': True},
            'organizations': {'required': False, 'allow_null': True},
            'coCurricular': {'required': False, 'allow_null': True},
            'declarations': {'required': False, 'allow_null': True},
        }

    def validate(self, data):
        # Remove this validation since JSONField already handles it
        # The data here will be JSON strings, not lists
        return data