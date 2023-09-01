from .models import *
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Buyerdataform(ModelForm):
  class Meta:
    model = Buyerdata
    fields = '__all__'
    
class storeform(ModelForm):
  class Meta:
    model = store
    fields = '__all__'