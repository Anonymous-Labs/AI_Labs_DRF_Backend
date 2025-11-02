from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Workspace
from .serializers import WorkspaceSerializer


class WorkspaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CRUD operations on Workspace.
    
    User information is automatically retrieved from the JWT Authorization token.
    Users can only access their own workspaces.
    """
    serializer_class = WorkspaceSerializer

    def get_queryset(self):
        """
        Filter workspaces to only show those belonging to the authenticated user.
        """
        return Workspace.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the user to the authenticated user from the JWT token.
        """
        serializer.save(user=self.request.user)
