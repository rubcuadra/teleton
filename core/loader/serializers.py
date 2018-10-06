from rest_framework import serializers
from .models import *

class BanamexSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Banamex
        fields = '__all__'

class SorianaSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Soriana
        fields = '__all__'
