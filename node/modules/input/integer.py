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