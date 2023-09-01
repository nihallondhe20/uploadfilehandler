from django.db import models

# Create your models here.


class store(models.Model):
    name = models.CharField(max_length=20)
    file = models.FileField(upload_to='store/excel/')
    
    def __str__(self):
        return self.name + " store name  " +str(self.id)
    

class Buyerdata(models.Model):
  date =  models.CharField(max_length=200)
  buyer = models.CharField(max_length=200)
  address = models.CharField(max_length=200)
  total_amount = models.CharField(max_length=200)
  def __str__(self):
        return self.buyer 