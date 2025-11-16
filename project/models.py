from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Workspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspaces')
    name = models.CharField(max_length=255)
    edges = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    def get_all_node_ids(self):
        """Get all node IDs from all node types in this workspace."""
        node_ids = set()
        node_ids.update(self.integer_nodes.values_list('id', flat=True))
        node_ids.update(self.text_nodes.values_list('id', flat=True))
        node_ids.update(self.dataset_nodes.values_list('id', flat=True))
        node_ids.update(self.feature_selection_nodes.values_list('id', flat=True))
        node_ids.update(self.train_test_split_nodes.values_list('id', flat=True))
        node_ids.update(self.linear_regression_nodes.values_list('id', flat=True))
        node_ids.update(self.prediction_nodes.values_list('id', flat=True))
        node_ids.update(self.accuracy_nodes.values_list('id', flat=True))
        node_ids.update(self.add2int_nodes.values_list('id', flat=True))
        return node_ids
