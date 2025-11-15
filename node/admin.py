from django.contrib import admin
from node.modules.input.integer import Integer
from node.modules.output.text import Text
from node.modules.input.dataset import Dataset
from node.modules.preprocessing.feature_selection import FeatureSelection
from node.modules.preprocessing.train_test_split import TrainTestSplit
from node.modules.model.linear_regression import LinearRegression
from node.modules.evaluation.predict import Predict
from node.modules.evaluation.accuracy import Accuracy
from node.modules.arithmetic.add2int import Add2Int


@admin.register(Integer)
class IntegerAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "number")
    search_fields = ("id",)
    list_filter = ("workspace",)


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "text")
    search_fields = ("id",)
    list_filter = ("workspace",)


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "file_path", "rows", "columns")
    search_fields = ("id", "file_path")
    list_filter = ("workspace",)


@admin.register(FeatureSelection)
class FeatureSelectionAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "target_column", "n_features")
    search_fields = ("id", "target_column")
    list_filter = ("workspace",)


@admin.register(TrainTestSplit)
class TrainTestSplitAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "test_size", "train_samples", "test_samples")
    search_fields = ("id",)
    list_filter = ("workspace",)


@admin.register(LinearRegression)
class LinearRegressionAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "fit_intercept", "n_features")
    search_fields = ("id",)
    list_filter = ("workspace",)


@admin.register(Predict)
class PredictAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "n_predictions", "has_probabilities")
    search_fields = ("id",)
    list_filter = ("workspace",)


@admin.register(Accuracy)
class AccuracyAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "metric_type", "metric_value")
    search_fields = ("id", "metric_type")
    list_filter = ("workspace",)


@admin.register(Add2Int)
class Add2IntAdmin(admin.ModelAdmin):
    list_display = ("id", "workspace", "sum")
    search_fields = ("id",)
    list_filter = ("workspace",)
