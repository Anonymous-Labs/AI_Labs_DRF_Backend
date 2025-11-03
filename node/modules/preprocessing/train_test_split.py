from django.db import models
from node.models import BaseNode

from node.services.preprocessing.train_test_split import train_test_split as split_data

class TrainTestSplit(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='train_test_split_nodes'
    )
    test_size = models.FloatField(default=0.2)
    train_samples = models.IntegerField()
    test_samples = models.IntegerField()

    @staticmethod
    def execute(payload):
        # Extract metadata and parameters
        metadata = payload.get("metadata", {})
        params = {
            key.split("_")[-1]: value
            for key, value in payload.items()
            if key.startswith("I_")
        }

        # Perform train-test split
        result = split_data(
            X=params.get('X'),
            y=params.get('y'),
            test_size=params.get('test_size', 0.2)
        )

        # Check if we're updating or creating
        instance_id = metadata.get("id")
        if instance_id:
            # Update existing object
            try:
                tts_instance = TrainTestSplit.objects.get(id=instance_id)
                tts_instance.test_size = params.get('test_size', 0.2)
                tts_instance.train_samples = len(result['X_train'])
                tts_instance.test_samples = len(result['X_test'])
                tts_instance.save()
            except TrainTestSplit.DoesNotExist:
                # Fallback: if object not found, create a new one
                tts_instance = TrainTestSplit.objects.create(
                    test_size=params.get('test_size', 0.2),
                    train_samples=len(result['X_train']),
                    test_samples=len(result['X_test'])
                )
        else:
            # Create new object
            tts_instance = TrainTestSplit.objects.create(
                test_size=params.get('test_size', 0.2),
                train_samples=len(result['X_train']),
                test_samples=len(result['X_test'])
            )

        # Serialize all fields dynamically
        data = {
            field.name: getattr(tts_instance, field.name)
            for field in tts_instance._meta.fields
        }

        # Add split datasets to response
        data.update(result)  # Adds X_train, X_test, y_train, y_test to response

        return data
