from rest_framework import serializers
from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        # Get user from request (set by authentication)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
