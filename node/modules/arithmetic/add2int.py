from django.db import models
from node.models import BaseNode

from node.services.arithmetic.add2int import add_two_numbers

class Add2Int(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='add2int_nodes'
    )
    sum = models.IntegerField()

    @staticmethod
    def execute(payload):
        # Extract metadata and parameters
        metadata = payload.get("metadata", {})
        params = {
            key.split("_")[-1]: value
            for key, value in payload.items()
            if key.startswith("I_")
        }

        # Perform the computation
        result_sum = add_two_numbers(**params)

        # Check if we're updating or creating
        instance_id = metadata.get("id")
        if instance_id:
            # Update existing object
            try:
                add2int_instance = Add2Int.objects.get(id=instance_id)
                add2int_instance.sum = result_sum
                add2int_instance.save()
            except Add2Int.DoesNotExist:
                # Fallback: if object not found, create a new one
                add2int_instance = Add2Int.objects.create(sum=result_sum)
        else:
            # Create new object
            add2int_instance = Add2Int.objects.create(sum=result_sum)

        # Serialize all fields dynamically
        data = {
            field.name: getattr(add2int_instance, field.name)
            for field in add2int_instance._meta.fields
        }

        return data