from django.db import models
from node.models import BaseNode
import pandas as pd

from node.services.input.dataset import dataset as load_dataset

class Dataset(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='dataset_nodes'
    )
    file_path = models.CharField(max_length=255)
    rows = models.IntegerField()
    columns = models.IntegerField()

    @staticmethod
    def execute(payload):
        # Extract metadata and parameters
        metadata = payload.get("metadata", {})
        params = {
            key.split("_")[-1]: value
            for key, value in payload.items()
            if key.startswith("I_")
        }

        # Load the dataset
        df = load_dataset(params.get('file_path'))

        # Check if we're updating or creating
        instance_id = metadata.get("id")
        if instance_id:
            # Update existing object
            try:
                dataset_instance = Dataset.objects.get(id=instance_id)
                dataset_instance.file_path = params.get('file_path')
                dataset_instance.rows = df.shape[0]
                dataset_instance.columns = df.shape[1]
                dataset_instance.save()
            except Dataset.DoesNotExist:
                # Fallback: if object not found, create a new one
                dataset_instance = Dataset.objects.create(
                    file_path=params.get('file_path'),
                    rows=df.shape[0],
                    columns=df.shape[1]
                )
        else:
            # Create new object
            dataset_instance = Dataset.objects.create(
                file_path=params.get('file_path'),
                rows=df.shape[0],
                columns=df.shape[1]
            )

        # Serialize all fields dynamically
        data = {
            field.name: getattr(dataset_instance, field.name)
            for field in dataset_instance._meta.fields
        }

        # Add the DataFrame to the response
        data['data'] = df.to_dict(orient='records')

        return data
