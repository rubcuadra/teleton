from rest_framework import serializers
from .models import *

class BanamexSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Banamex
        fields = '__all__'
        depth = 1
        
class SorianaSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Soriana
        fields = '__all__'
        depth = 1

class CentrosSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Centros
        fields = '__all__'

class PacientesSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Pacientes
        fields = '__all__'

class TelmexSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Telmex
        fields = '__all__'

class FarmaciaAhorroSerializer(serializers.ModelSerializer):
    class Meta:    
        model = FarmaciaAhorro
        fields = '__all__'

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Estado
        fields = '__all__'

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Income
        fields = '__all__'
        depth=1