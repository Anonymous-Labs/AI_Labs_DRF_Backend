from rest_framework import serializers

from node.modules.input.integer import Integer
from node.modules.output.text import Text
from node.modules.input.dataset import Dataset
from node.modules.preprocessing.feature_selection import FeatureSelection
from node.modules.preprocessing.train_test_split import TrainTestSplit
from node.modules.model.linear_regression import LinearRegression
from node.modules.evaluation.predict import Predict
from node.modules.evaluation.accuracy import Accuracy
from node.modules.arithmetic.add2int import Add2Int


class IntegerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Integer
        fields = "__all__"


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = "__all__"


class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = "__all__"


class FeatureSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureSelection
        fields = "__all__"


class TrainTestSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainTestSplit
        fields = "__all__"


class LinearRegressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LinearRegression
        fields = "__all__"


class PredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predict
        fields = "__all__"


class AccuracySerializer(serializers.ModelSerializer):
    class Meta:
        model = Accuracy
        fields = "__all__"


class Add2IntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Add2Int
        fields = "__all__"


