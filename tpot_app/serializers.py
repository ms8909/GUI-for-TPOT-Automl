from rest_framework import serializers
from .models import *

class DatasetSerializers(serializers.ModelSerializer):
    class Meta:
        model= Dataset
        fields= ('id', 'address', 'y_variable')


class TrainsetSerializers(serializers.ModelSerializer):
    class Meta:
        model= Training
        fields= ('id', 'params', 'status', 'dataset')

