from django.urls import path, include

from . import views
from rest_framework import routers
from rest_framework import renderers




router= routers.DefaultRouter()
router.register('dataset', views.DatasetViewSet)
router.register('train', views.TrainsetViewSet)




urlpatterns = [

    path('train_start/', views.train_start, name='train_start'),
    path('train_details/', views.train_details, name='train_details'),
    path('model_deploy/', views.model_deploy, name='model_deploy'),
    path('model_predict/', views.model_predict, name='model_predict'),
    path('', include(router.urls)),



]


