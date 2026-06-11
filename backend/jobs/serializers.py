from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'status', 'category', 'address', 'city', 
            'state', 'start_date', 'end_date', 'description', 
            'profile_picture', 'order', 'created_at'
        ]
        read_only_fields = ['id', 'order', 'created_at']
