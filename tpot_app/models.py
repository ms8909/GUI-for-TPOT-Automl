from django.db import models
# from django.contrib.postgres.fields import JSONField


# Create your models here.






class Dataset(models.Model):
    address = models.TextField(blank=True, null=True)
    y_variable = models.TextField(blank=True, null=True)



class Training(models.Model):
    params = models.TextField(blank=True, null=True)
    training_id = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50,default="NOTSTARTED" )
    dataset= models.ForeignKey(Dataset, on_delete=models.CASCADE, null=True, blank=True)
    model_address = models.TextField(blank=True, null=True) #address on S3



