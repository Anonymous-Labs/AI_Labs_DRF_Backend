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