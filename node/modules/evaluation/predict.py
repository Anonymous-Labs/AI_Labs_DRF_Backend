from django.db import models
from node.models import BaseNode
import pandas as pd

from node.services.evaluation.predict import predict as make_prediction

class Predict(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='prediction_nodes'
    )
    n_predictions = models.IntegerField()
    has_probabilities = models.BooleanField(default=False)

    @staticmethod
    def execute(payload):
        # Extract metadata and parameters
        metadata = payload.get("metadata", {})
        params = {
            key.split("_")[-1]: value
            for key, value in payload.items()
            if key.startswith("I_")
        }

        # Make predictions
        result = make_prediction(
            model=params.get('model'),
            X=params.get('X')
        )

        predictions = result['predictions']
        prediction_probs = result['prediction_probs']

        # Check if we're updating or creating
        instance_id = metadata.get("id")
        if instance_id:
            # Update existing object
            try:
                predict_instance = Predict.objects.get(id=instance_id)
                predict_instance.n_predictions = len(predictions)
                predict_instance.has_probabilities = prediction_probs is not None
                predict_instance.save()
            except Predict.DoesNotExist:
                # Fallback: if object not found, create a new one
                predict_instance = Predict.objects.create(
                    n_predictions=len(predictions),
                    has_probabilities=prediction_probs is not None
                )
        else:
            # Create new object
            predict_instance = Predict.objects.create(
                n_predictions=len(predictions),
                has_probabilities=prediction_probs is not None
            )

        # Serialize all fields dynamically
        data = {
            field.name: getattr(predict_instance, field.name)
            for field in predict_instance._meta.fields
        }

        # Add predictions to response
        data['predictions'] = predictions.to_dict()
        if prediction_probs is not None:
            data['prediction_probs'] = prediction_probs.to_dict()

        return data
