from django.db import models
from node.models import BaseNode

class Integer(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='integer_nodes'
    )
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)

    @staticmethod
    def execute(payload):
        # Extract metadata and parameters
        metadata = payload.get("metadata", {})

        params = {
            key.split("_")[-1]: value
            for key, value in metadata.items()
            if key.startswith("I_")
        }

        # Extract the number parameter
        number = params.get("number")
        if number is None:
            raise ValueError("The 'number' parameter is required.")

        # Extract the workspace ID
        workspace_id = payload.get("workspace")
        if workspace_id is None:
            raise ValueError("The 'workspace' parameter is required.")

        # Check if we're updating or creating
        instance_id = metadata.get("id")
        if instance_id:
            # Update existing object
            try:
                integer_instance = Integer.objects.get(id=instance_id, workspace_id=workspace_id)
                integer_instance.number = number
                integer_instance.save()
            except Integer.DoesNotExist:
                # Fallback: if object not found, create a new one
                integer_instance = Integer.objects.create(number=number, workspace_id=workspace_id)
        else:
            # Create new object
            integer_instance = Integer.objects.create(number=number, workspace_id=workspace_id)

        # Serialize all fields dynamically
        data = {
            field.name: getattr(integer_instance, field.name)
            for field in integer_instance._meta.fields
        }
        
        data["workspace"] = integer_instance.workspace.id

        return data