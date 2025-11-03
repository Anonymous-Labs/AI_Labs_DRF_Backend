from django.db import models
from node.models import BaseNode

from node.services.model.linear_regression import linear_regression as train_linear_regression

class LinearRegression(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='linear_regression_nodes'
    )
    fit_intercept = models.BooleanField(default=True)
    n_features = models.IntegerField()
    
    @staticmethod
    def execute(payload):
        # Extract metadata and parameters
        metadata = payload.get("metadata", {})
        params = {
            key.split("_")[-1]: value
            for key, value in payload.items()
            if key.startswith("I_")
        }

        # Train the model
        model = train_linear_regression(
            X_train=params.get('X_train'),
            y_train=params.get('y_train'),
            fit_intercept=params.get('fit_intercept', True)
        )

        # Check if we're updating or creating
        instance_id = metadata.get("id")
        if instance_id:
            # Update existing object
            try:
                lr_instance = LinearRegression.objects.get(id=instance_id)
                lr_instance.fit_intercept = params.get('fit_intercept', True)
                lr_instance.n_features = params.get('X_train').shape[1]
                lr_instance.save()
            except LinearRegression.DoesNotExist:
                # Fallback: if object not found, create a new one
                lr_instance = LinearRegression.objects.create(
                    fit_intercept=params.get('fit_intercept', True),
                    n_features=params.get('X_train').shape[1]
                )
        else:
            # Create new object
            lr_instance = LinearRegression.objects.create(
                fit_intercept=params.get('fit_intercept', True),
                n_features=params.get('X_train').shape[1]
            )

        # Serialize all fields dynamically
        data = {
            field.name: getattr(lr_instance, field.name)
            for field in lr_instance._meta.fields
        }

        # Add model parameters to response
        data['coefficients'] = model.coef_.tolist()
        data['intercept'] = float(model.intercept_) if model.fit_intercept else 0.0
        data['model'] = model  # The trained model object

        return data
