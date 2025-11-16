from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Workspace
from .serializers import WorkspaceSerializer, EdgeSerializer
import uuid

from node.serializers import (
    IntegerSerializer,
    TextSerializer,
    DatasetSerializer,
    FeatureSelectionSerializer,
    TrainTestSplitSerializer,
    LinearRegressionSerializer,
    PredictSerializer,
    AccuracySerializer,
    Add2IntSerializer,
)


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

    @action(detail=True, methods=['get'])
    def graph(self, request, pk=None):
        """
        Returns a detailed graph of all nodes and edges in the workspace, organized by type.
        """
        workspace = get_object_or_404(Workspace, pk=pk, user=request.user)
        
        # Collect all nodes by type
        graph_data = {
            'workspace_id': workspace.id,
            'workspace_name': workspace.name,
            'nodes': {
                'integer': IntegerSerializer(workspace.integer_nodes.all(), many=True).data,
                'text': TextSerializer(workspace.text_nodes.all(), many=True).data,
                'dataset': DatasetSerializer(workspace.dataset_nodes.all(), many=True).data,
                'featureSelection': FeatureSelectionSerializer(workspace.feature_selection_nodes.all(), many=True).data,
                'trainTestSplit': TrainTestSplitSerializer(workspace.train_test_split_nodes.all(), many=True).data,
                'linearRegression': LinearRegressionSerializer(workspace.linear_regression_nodes.all(), many=True).data,
                'predict': PredictSerializer(workspace.prediction_nodes.all(), many=True).data,
                'evaluation': AccuracySerializer(workspace.accuracy_nodes.all(), many=True).data,
                'add2int': Add2IntSerializer(workspace.add2int_nodes.all(), many=True).data,
            },
            'edges': workspace.edges if workspace.edges else []
        }
        
        return Response(graph_data)

    @action(detail=True, methods=['post'], url_path='edges')
    def create_edge(self, request, pk=None):
        """
        Create a new edge in the workspace.
        POST /api/project/workspaces/{id}/edges/
        """
        workspace = get_object_or_404(Workspace, pk=pk, user=request.user)
        
        serializer = EdgeSerializer(data=request.data, context={'workspace': workspace})
        serializer.is_valid(raise_exception=True)
        
        edge_data = serializer.validated_data
        
        # Generate edge_id if not provided
        if not edge_data.get('edge_id'):
            edge_data['edge_id'] = f"e-{edge_data['source_id']}-{edge_data['target_id']}-{uuid.uuid4().hex[:8]}"
        
        # Check if edge already exists
        edges = workspace.edges if workspace.edges else []
        for edge in edges:
            if (edge.get('source_id') == edge_data['source_id'] and 
                edge.get('target_id') == edge_data['target_id'] and
                edge.get('source_handle') == edge_data['source_handle'] and
                edge.get('target_handle') == edge_data['target_handle']):
                return Response(
                    {'error': 'Edge already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Add edge to workspace
        edges.append(edge_data)
        workspace.edges = edges
        workspace.save()
        
        return Response(edge_data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='edges/(?P<edge_id>[^/.]+)')
    def update_edge(self, request, pk=None, edge_id=None):
        """
        Update an existing edge in the workspace.
        PATCH /api/project/workspaces/{id}/edges/{edge_id}/
        """
        workspace = get_object_or_404(Workspace, pk=pk, user=request.user)
        
        edges = workspace.edges if workspace.edges else []
        edge_index = None
        
        # Find edge by edge_id or by source_id/target_id combination
        for i, edge in enumerate(edges):
            if edge.get('edge_id') == edge_id:
                edge_index = i
                break
        
        if edge_index is None:
            return Response(
                {'error': 'Edge not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update edge data
        existing_edge = edges[edge_index]
        serializer = EdgeSerializer(
            existing_edge,
            data=request.data,
            partial=True,
            context={'workspace': workspace}
        )
        serializer.is_valid(raise_exception=True)
        
        # Preserve edge_id if not being updated
        updated_edge = serializer.validated_data
        if 'edge_id' not in updated_edge:
            updated_edge['edge_id'] = existing_edge.get('edge_id', edge_id)
        
        edges[edge_index] = updated_edge
        workspace.edges = edges
        workspace.save()
        
        return Response(updated_edge)

    @action(detail=True, methods=['delete'], url_path='edges/(?P<edge_id>[^/.]+)')
    def delete_edge(self, request, pk=None, edge_id=None):
        """
        Delete an edge from the workspace.
        DELETE /api/project/workspaces/{id}/edges/{edge_id}/
        """
        workspace = get_object_or_404(Workspace, pk=pk, user=request.user)
        
        edges = workspace.edges if workspace.edges else []
        edge_index = None
        
        # Find edge by edge_id
        for i, edge in enumerate(edges):
            if edge.get('edge_id') == edge_id:
                edge_index = i
                break
        
        if edge_index is None:
            return Response(
                {'error': 'Edge not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Remove edge
        deleted_edge = edges.pop(edge_index)
        workspace.edges = edges
        workspace.save()
        
        return Response(
            {'message': 'Edge deleted successfully.', 'deleted_edge': deleted_edge},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='edges/delete')
    def delete_edge_by_nodes(self, request, pk=None):
        """
        Delete an edge by source_id and target_id.
        POST /api/project/workspaces/{id}/edges/delete/
        Body: {"source_id": 4, "target_id": 3}
        """
        workspace = get_object_or_404(Workspace, pk=pk, user=request.user)
        
        source_id = request.data.get('source_id')
        target_id = request.data.get('target_id')
        
        if source_id is None or target_id is None:
            return Response(
                {'error': 'Both source_id and target_id are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        edges = workspace.edges if workspace.edges else []
        edge_index = None
        
        # Find edge by source_id and target_id
        for i, edge in enumerate(edges):
            if (edge.get('source_id') == source_id and 
                edge.get('target_id') == target_id):
                edge_index = i
                break
        
        if edge_index is None:
            return Response(
                {'error': 'Edge not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Remove edge
        deleted_edge = edges.pop(edge_index)
        workspace.edges = edges
        workspace.save()
        
        return Response(
            {'message': 'Edge deleted successfully.', 'deleted_edge': deleted_edge},
            status=status.HTTP_200_OK
        )
