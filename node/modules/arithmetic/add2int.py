from django.db import models
from node.models import BaseNode

from node.services.arithmetic.add2int import add_two_numbers

class Add2Int(BaseNode):
    workspace = models.ForeignKey(
        'project.Workspace',
        on_delete=models.CASCADE,
        related_name='add2int_nodes'
    )
    sum = models.IntegerField(blank=True, null=True, default=0)


    @staticmethod
    def execute(payload, instance_id=None):
        # Extract parameters from payload
        # Expected format: I_Add2Int_num1, I_Add2Int_num2
        params = {}
        for key, value in payload.items():
            if key.startswith("I_Add2Int_"):
                # Extract parameter name (e.g., "num1" from "I_Add2Int_num1")
                param_name = key.replace("I_Add2Int_", "")
                params[param_name] = value

        # Validate required parameters
        if 'num1' not in params or 'num2' not in params:
            raise ValueError("Both 'I_Add2Int_num1' and 'I_Add2Int_num2' are required in the payload.")

        # Perform the computation
        result_sum = add_two_numbers(num1=params['num1'], num2=params['num2'])

        # Use instance_id from parameter or try to get from metadata
        if not instance_id:
            metadata = payload.get("metadata", {})
            instance_id = metadata.get("id")

        if instance_id:
            # Update existing object
            try:
                add2int_instance = Add2Int.objects.get(id=instance_id)
                add2int_instance.sum = result_sum
                add2int_instance.save()
            except Add2Int.DoesNotExist:
                raise ValueError(f"Add2Int instance with id={instance_id} not found.")
        else:
            raise ValueError("Instance ID is required. Either pass instance_id parameter or include it in metadata.")

        # Return the sum and instance data
        return {
            'id': add2int_instance.id,
            'sum': add2int_instance.sum,
            'workspace': add2int_instance.workspace.id
        }