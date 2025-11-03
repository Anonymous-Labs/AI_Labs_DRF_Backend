from django.db import models
from node.models import BaseNode

from node.services.evaluation.accuracy import accuracy_metric

class Accuracy(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='accuracy_nodes'
    )
    metric_type = models.CharField(max_length=10)
    metric_value = models.FloatField()

    @staticmethod
    def execute(payload):
        # Extract metadata and parameters
        metadata = payload.get("metadata", {})
        params = {
            key.split("_")[-1]: value
            for key, value in payload.items()
            if key.startswith("I_")
        }

        # Calculate the accuracy metric
        result = accuracy_metric(
            y_true=params.get('y_true'),
            y_pred=params.get('y_pred'),
            metric_type=params.get('metric_type', 'r2')
        )

        # Check if we're updating or creating
        instance_id = metadata.get("id")
        if instance_id:
            # Update existing object
            try:
                accuracy_instance = Accuracy.objects.get(id=instance_id)
                accuracy_instance.metric_type = params.get('metric_type', 'r2')
                accuracy_instance.metric_value = result
                accuracy_instance.save()
            except Accuracy.DoesNotExist:
                # Fallback: if object not found, create a new one
                accuracy_instance = Accuracy.objects.create(
                    metric_type=params.get('metric_type', 'r2'),
                    metric_value=result
                )
        else:
            # Create new object
            accuracy_instance = Accuracy.objects.create(
                metric_type=params.get('metric_type', 'r2'),
                metric_value=result
            )

        # Serialize all fields dynamically
        data = {
            field.name: getattr(accuracy_instance, field.name)
            for field in accuracy_instance._meta.fields
        }

        return data
