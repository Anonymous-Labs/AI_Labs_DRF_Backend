from django.db import models
from node.models import BaseNode
import json

from node.services.preprocessing.feature_selection import feature_selection as select_features

class FeatureSelection(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='feature_selection_nodes'
    )
    target_column = models.CharField(max_length=255)
    n_features = models.IntegerField()
    feature_columns = models.TextField()  # JSON list of feature columns

    @staticmethod
    def execute(payload):
        # Extract metadata and parameters
        metadata = payload.get("metadata", {})
        params = {
            key.split("_")[-1]: value
            for key, value in payload.items()
            if key.startswith("I_")
        }

        # Select features
        result = select_features(
            dataframe=params.get('dataframe'),
            target_column=params.get('target_column'),
            feature_columns=params.get('feature_columns')
        )

        # Check if we're updating or creating
        instance_id = metadata.get("id")
        if instance_id:
            # Update existing object
            try:
                fs_instance = FeatureSelection.objects.get(id=instance_id)
                fs_instance.target_column = params.get('target_column')
                fs_instance.n_features = len(params.get('feature_columns'))
                fs_instance.feature_columns = json.dumps(params.get('feature_columns'))
                fs_instance.save()
            except FeatureSelection.DoesNotExist:
                # Fallback: if object not found, create a new one
                fs_instance = FeatureSelection.objects.create(
                    target_column=params.get('target_column'),
                    n_features=len(params.get('feature_columns')),
                    feature_columns=json.dumps(params.get('feature_columns'))
                )
        else:
            # Create new object
            fs_instance = FeatureSelection.objects.create(
                target_column=params.get('target_column'),
                n_features=len(params.get('feature_columns')),
                feature_columns=json.dumps(params.get('feature_columns'))
            )

        # Serialize all fields dynamically
        data = {
            field.name: getattr(fs_instance, field.name)
            for field in fs_instance._meta.fields
        }

        # Add selected features and target to response
        data['X'] = result['X']
        data['y'] = result['y']
        data['feature_columns'] = json.loads(data['feature_columns'])  # Convert back to list

        return data
