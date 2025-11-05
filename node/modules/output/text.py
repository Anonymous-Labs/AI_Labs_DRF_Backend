from django.db import models
from node.models import BaseNode

class Text(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='text_nodes'
    )
    text = models.TextField()

    def __str__(self):
        return str(self.text)

    @staticmethod
    def execute(payload):
        # Extract metadata and parameters
        metadata = payload.get("metadata", {})
        params = {
            key.split("_")[-1]: value
            for key, value in payload.items()
            if key.startswith("I_")
        }

        # Extract the text parameter
        text = params.get("text")
        if text is None:
            raise ValueError("The 'text' parameter is required.")

        # Check if we're updating or creating
        instance_id = metadata.get("id")
        if instance_id:
            # Update existing object
            try:
                text_instance = Text.objects.get(id=instance_id)
                text_instance.text = text
                text_instance.save()
            except Text.DoesNotExist:
                # Fallback: if object not found, create a new one
                text_instance = Text.objects.create(text=text)
        else:
            # Create new object
            text_instance = Text.objects.create(text=text)

        # Serialize all fields dynamically
        data = {
            field.name: getattr(text_instance, field.name)
            for field in text_instance._meta.fields
        }

        return data