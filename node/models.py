from django.db import models

class BaseNode(models.Model):
    """
    Abstract base model for all nodes.
    Contains common fields shared by all node types.
    """
    id = models.AutoField(primary_key=True)
    position_x = models.FloatField(default=0.0, help_text="X position in canvas")
    position_y = models.FloatField(default=0.0, help_text="Y position in canvas")

    @staticmethod
    def execute(payload):
        raise NotImplementedError("Subclasses must override the execute method.")

    class Meta:
        abstract = True

from .modules.arithmetic.add2int import Add2Int
from .modules.input.integer import Integer
from .modules.output.text import Text