# -*- coding: utf-8 -*- 
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

from django.db.models import Sum


class Estado(models.Model):
    _id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    lat = models.DecimalField(max_digits=12, decimal_places=8)
    lng = models.DecimalField(max_digits=12, decimal_places=8)

    @staticmethod
    def BanamexParser(estadoBanamex):
        BANAMEX_PARSER = { 1:2,2:3,3:4,4:5,7:8,8:9,5:6,6:7,9:1,15:11,11:12,12:13,13:14,14:15 }
        if estadoBanamex in BANAMEX_PARSER: return BANAMEX_PARSER[estadoBanamex]
        return estadoBanamex #it is already ok
        
    @staticmethod
    def TelmexParser(estadoTelmex):
        return {
            "Aguascalientes":2,
            "Baja California Norte":3,
            "Baja California Sur":4,
            "Campeche":5,
            "Chiapas":8,
            "Chihuahua":9,
            "Coahuila":6,
            "Colima":7,
            "DF":1,
            "Durango":10,
            "Estado de Mxico":11,
            "Guanajuato":12,
            "Guerrero":13,
            "Hidalgo":14,
            "Jalisco":15,
            "Michoacn":16,
            "Morelos":17,
            "Nayarit":18,
            "Nuevo Len":19,
            "Oaxaca":20,
            "Puebla":21,
            "Quertaro":22,
            "Quintana Roo":23,
            "San Luis Potos":24,
            "Sinaloa":25,
            "Sonora":26,
            "Tabasco":27,
            "Tamaulipas":28,
            "Tlaxcala":29,
            "Veracruz":30,
            "Yucatn":31,
            "Zacatecas":32,
            "TOTALES":-1,
        }[estadoTelmex]

class BanamexManager(models.Manager):
    def get_total_amount(self): return self.aggregate(Sum('Monto'))["Monto__sum"]

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
    Autorizacion = models.BigIntegerField(primary_key=True) #12 digits, integer has 10
    Monto = models.DecimalField(max_digits=15, decimal_places=2)
    Estado = models.ForeignKey(Estado)
    objects = BanamexManager()

    @staticmethod
    def getFecha(fecha,hora): #aaaammdd, hhmm
        fecha = str(fecha)
        hora = str(hora)
        o = [ fecha[:4],fecha[4:6],fecha[6:],hora[:2],hora[2:] ]
        return datetime(*[int(k) for k in o])
    
class Soriana(models.Model):
    Donadores = models.BigIntegerField() 
    Fecha = models.DateTimeField(auto_now=False) #fecha y hora
    Tienda = models.IntegerField()
    Monto = models.DecimalField(max_digits=16, decimal_places=8)
    
    @staticmethod
    def getFecha(fecha): #aaaa-mm-dd hh:mmtt EJ. 20161211   2:00AM
        return datetime.strptime(fecha,"%Y%m%d   %I:%M%p")
        
    class Meta:
        unique_together = (("Fecha", "Tienda"),)

class TelmexManager(models.Manager):
    def get_total_amount(self): 
        newest = self.filter(Fecha=self.latest().Fecha)
        return sum(n.Importe for n in newest)

class Telmex(models.Model):
    Fecha = models.DateTimeField(auto_now=False) #fecha y horaT
    Estado = models.ForeignKey(Estado)
    Llamadas = models.IntegerField()
    Importe = models.DecimalField(max_digits=13, decimal_places=3)
    Porcentaje = models.DecimalField(max_digits=8, decimal_places=4) #Por monto acumulado...wtf?
    objects = TelmexManager()

    class Meta:
        unique_together = (("Fecha", "Estado"),)
        get_latest_by = 'Fecha'

class Pacientes(models.Model):
    FL_PACIENTE = models.BigIntegerField(primary_key=True,verbose_name='id') 
    NB_ALIAS = models.CharField(max_length=40,verbose_name='alias') 
    EDAD = models.CharField(max_length=10,verbose_name='edad')
    NB_ENFERMEDAD = models.CharField(max_length=255,verbose_name='enfermedad')
    #Egresos
    CL_ESTATUS = models.CharField(max_length=1,verbose_name='estatus', blank=True, null=True)
    DS_LOGROS = models.CharField(max_length=1000,verbose_name='logros', blank=True, null=True)
    DS_TESTIMONIOS = models.CharField(max_length=1000,verbose_name='testimonios', blank=True, null=True)

class Centros(models.Model):
    name = models.CharField(max_length=50) 
    required = models.BigIntegerField(verbose_name='Recursos necesarios 2018')
    promised = models.BigIntegerField(verbose_name='Ingresos comprometidos')
    estimated_accomplishment = models.IntegerField(verbose_name='\% esperado de cumplimiento')
    estimated = models.BigIntegerField(verbose_name='Ingresos esperados')
    required_event = models.BigIntegerField(verbose_name='Recursos necesarios en evento Teleton')
    capacity = models.IntegerField(verbose_name='Capacidad de pacientes')
    anual_cost = models.IntegerField(verbose_name='Costo anual promedio por paciente')
    amount_help = models.IntegerField(verbose_name='Numero de pacientes por cubrir con donativos')
