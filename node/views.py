from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response

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

from node.modules.input.integer import Integer
from node.modules.output.text import Text
from node.modules.input.dataset import Dataset
from node.modules.preprocessing.feature_selection import FeatureSelection
from node.modules.preprocessing.train_test_split import TrainTestSplit
from node.modules.model.linear_regression import LinearRegression
from node.modules.evaluation.predict import Predict
from node.modules.evaluation.accuracy import Accuracy
from node.modules.arithmetic.add2int import Add2Int

class IntegerViewSet(viewsets.ModelViewSet):
    queryset = Integer.objects.all()
    serializer_class = IntegerSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=True) 
    def execute(self, request, pk=None): 
        result = Integer.execute(request.data)
        return Response(result)

class TextViewSet(viewsets.ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False)
    def execute(self, request):
        result = Text.execute(request.data)
        return Response(result)

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False)
    def execute(self, request):
        result = Dataset.execute(request.data)
        return Response(result)

class FeatureSelectionViewSet(viewsets.ModelViewSet):
    queryset = FeatureSelection.objects.all()
    serializer_class = FeatureSelectionSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False)
    def execute(self, request):
        result = FeatureSelection.execute(request.data)
        return Response(result)

class TrainTestSplitViewSet(viewsets.ModelViewSet):
    queryset = TrainTestSplit.objects.all()
    serializer_class = TrainTestSplitSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False)
    def execute(self, request):
        result = TrainTestSplit.execute(request.data)
        return Response(result)

class LinearRegressionViewSet(viewsets.ModelViewSet):
    queryset = LinearRegression.objects.all()
    serializer_class = LinearRegressionSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False)
    def execute(self, request):
        result = LinearRegression.execute(request.data)
        return Response(result)

class PredictViewSet(viewsets.ModelViewSet):
    queryset = Predict.objects.all()
    serializer_class = PredictSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False)
    def execute(self, request):
        result = Predict.execute(request.data)
        return Response(result)

class AccuracyViewSet(viewsets.ModelViewSet):
    queryset = Accuracy.objects.all()
    serializer_class = AccuracySerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False)
    def execute(self, request):
        result = Accuracy.execute(request.data)
        return Response(result)

class Add2IntViewSet(viewsets.ModelViewSet):
    queryset = Add2Int.objects.all()
    serializer_class = Add2IntSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False)
    def execute(self, request):
        result = Add2Int.execute(request.data)
        return Response(result)
