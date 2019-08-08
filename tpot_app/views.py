from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, mixins
from rest_framework.generics import GenericAPIView, ListAPIView
from .models import *
from rest_framework.decorators import action, api_view
from django.http import JsonResponse
from .serializers import *
from rest_framework import renderers
from rest_framework.response import Response
from .tasks import *
from rest_framework import status

# Create your views here.

from dask.distributed import Client
client= Client()


class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializers

class TrainsetViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainsetSerializers






@api_view(['GET', 'POST'])
def train_start(request):
    if request.method == 'POST':

        # get inputs
        train_id = request.data.get('training_id', None)
        dataset_address = request.data.get('dataset_address', None)
        y_variable = request.data.get('y_variable', None)
        problem_type = request.data.get('problem_type', None)

        # check if training id is not in the dataset
        if train_id==None:
            return Response(data={'error': 'Something went wrong.', 'success': False, "code":401},
                            status=status.HTTP_200_OK)


        train_obj= Training.objects.filter(training_id= train_id)
        if len(train_obj)!= 0:
            # check if training is in process. Return status
            state= train_obj[0].status
            return Response(data={'error': 'Training was already started.', 'success': True, "code":200, 'training_status': state},
                            status=status.HTTP_200_OK)


        # start training
        train.send(train_id, dataset_address, y_variable, problem_type)

        return Response(data={'error': 'Training started successfully', 'success': True, "code":201},
                            status=status.HTTP_200_OK)



@api_view(['GET', 'POST'])
def train_details(request):
    if request.method == 'GET':

        return HttpResponse("Hello, we are in training details")



@api_view(['GET', 'POST'])
def model_deploy(request):
    if request.method == 'GET':
        return HttpResponse("Hello, we are in training details")



@api_view(['GET', 'POST'])
def model_predict(request):
    if request.method == 'POST':
        #get inputs
            # training iD and dataset ID will be provided by the user
        train_id = request.data.get('training_id', None)
        data_set = request.data.get('dataset', None)


        #load data, call preduct function, get results, and submit
        y_pred= predict(train_id, data_set)
        return Response(data={'error': 'Training started successfully', 'success': True, "code":201, "predictions": y_pred},
                            status=status.HTTP_200_OK)
