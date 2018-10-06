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

class CentrosSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Centros
        fields = '__all__'

class PacientesSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Pacientes
        fields = '__all__'