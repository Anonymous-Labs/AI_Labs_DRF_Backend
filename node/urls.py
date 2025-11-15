from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IntegerViewSet,
    TextViewSet,
    DatasetViewSet,
    FeatureSelectionViewSet,
    TrainTestSplitViewSet,
    LinearRegressionViewSet,
    PredictViewSet,
    AccuracyViewSet,
    Add2IntViewSet,
)

router = DefaultRouter()
router.register(r'integers', IntegerViewSet, basename='integer')
router.register(r'texts', TextViewSet, basename='text')
router.register(r'datasets', DatasetViewSet, basename='dataset')
router.register(r'feature-selections', FeatureSelectionViewSet, basename='featureselection')
router.register(r'train-test-splits', TrainTestSplitViewSet, basename='traintestsplit')
router.register(r'linear-regressions', LinearRegressionViewSet, basename='linearregression')
router.register(r'predicts', PredictViewSet, basename='predict')
router.register(r'accuracies', AccuracyViewSet, basename='accuracy')
router.register(r'add2ints', Add2IntViewSet, basename='add2int')

urlpatterns = [
    path('', include(router.urls)),
]