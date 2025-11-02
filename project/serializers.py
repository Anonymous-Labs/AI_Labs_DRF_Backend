from rest_framework import serializers
from .models import Workspace


class WorkspaceSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Workspace
        fields = ['id', 'name', 'user', 'user_email', 'user_username']
        read_only_fields = ['id', 'user']

    def create(self, validated_data):
        # Get user from request (set by authentication)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

