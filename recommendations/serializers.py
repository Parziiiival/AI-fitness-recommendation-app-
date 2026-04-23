from rest_framework import serializers
from .models import FitnessRecord


class FitnessRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessRecord
        fields = [
            'id', 'age', 'gender', 'height', 'weight', 'bmi',
            'goal', 'activity_level', 'experience_level',
            'workout', 'diet', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
