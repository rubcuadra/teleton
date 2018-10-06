from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
# from channels import Group
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from datetime import datetime
# from django.contrib.auth import get_user_model
import json

class Banamex(models.Model):
    MEDIO_CHOICE = (\
        (1, 'Sucs'),
        (2, 'Cats'),
        (3, 'Corr'),
        (4, 'Bnet'),
        (5, 'Tfer'),
        (6, 'Alcancias'),
        (7, 'Otro 7'),
        (8, 'Otro 8'),
        (9, 'Otro 9'),
    )

    TIPO_CHOICE = (
        (1, 'Efec'),
        (2, 'ChBx'),
        (3, 'ChOB'),
        (4, 'TBNX'),
        (5, 'TOBS'),
        (6, 'AMEX'),
        (7, 'Otro 7'),
        (8, 'Otro 8'),
        (9, 'Otro 9'),
    )

    Fecha = models.DateTimeField(auto_now=False) #fecha y hora
    Medio = models.IntegerField(choices=MEDIO_CHOICE)
    Tipo = models.IntegerField(choices=TIPO_CHOICE)
    Sucursal = models.IntegerField()
    Cuenta = models.IntegerField()
    Autorizacion = models.BigIntegerField() #12 digits, integer has 10
    Monto = models.DecimalField(max_digits=15, decimal_places=2)
    Estado = models.IntegerField()

    @staticmethod
    def getFecha(fecha,hora): #aaaammdd, hhmm
        fecha = str(fecha)
        hora = str(hora)
        o = [ fecha[:4],fecha[4:6],fecha[6:],hora[:2],hora[2:] ]
        return datetime(*[int(k) for k in o])
    
class Soriana(models.Model):
    Donadores = models.BigIntegerField(primary_key=True) #Llevar tracking del archivo acumulado
    Fecha = models.DateTimeField(auto_now=False) #fecha y hora
    Tienda = models.IntegerField()

    # FECHA|TIENDA|DONADORES|IMPORTE
