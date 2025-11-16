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


class EdgeSerializer(serializers.Serializer):
    """Serializer for edge creation and validation."""
    source_id = serializers.IntegerField()
    target_id = serializers.IntegerField()
    source_handle = serializers.CharField(max_length=100)
    target_handle = serializers.CharField(max_length=100)
    edge_id = serializers.CharField(required=False, allow_blank=True)  # Optional, for frontend-generated IDs

    def validate(self, attrs):
        """Validate that source and target nodes exist in the workspace."""
        workspace = self.context.get('workspace')
        if not workspace:
            raise serializers.ValidationError("Workspace context is required for edge validation.")
        
        node_ids = workspace.get_all_node_ids()
        
        if attrs['source_id'] not in node_ids:
            raise serializers.ValidationError(
                f"Source node with id={attrs['source_id']} does not exist in this workspace."
            )
        
        if attrs['target_id'] not in node_ids:
            raise serializers.ValidationError(
                f"Target node with id={attrs['target_id']} does not exist in this workspace."
            )
        
        if attrs['source_id'] == attrs['target_id']:
            raise serializers.ValidationError("Source and target nodes cannot be the same.")
        
        return attrs
