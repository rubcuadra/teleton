# -*- coding: utf-8 -*- 
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from codecs import EncodedFile, BOM_UTF8
import csv

FILE_HEADER = "fisier"

class BanamexUploadViewSet(APIView):
    def fix(self,row):
        row["Fecha"] = Banamex.getFecha(row["Fecha"],row["Hora"])
        del row["Hora"] #Useless
        return row

    def post(self,request):
        if FILE_HEADER in request.FILES:
            f = request.FILES[FILE_HEADER]
            if f:
                data = csv.DictReader( EncodedFile(f, 'utf8', "utf-8-sig") )
                for d in data:
                    print(d)
                    bs = BanamexSerializer(data=self.fix(d))
                    if bs.is_valid():
                        bs.save()
                return Response({"msg":"OK"}, status = status.HTTP_201_CREATED)
        return Response({"msg":"WRONG FILE"}, status=status.HTTP_400_BAD_REQUEST)

class SorianaUploadViewSet(APIView):
    def fix(self,row):
        row["Fecha"] = Banamex.getFecha(row["Fecha"],row["Hora"])
        del row["Hora"] #Useless
        return row

    def post(self,request):
        if FILE_HEADER in request.FILES:
            f = request.FILES[FILE_HEADER]
            if f:
                skip = 2
                line = ""
                for x in f.read():
                    if x == '\x00' or x == "\r": continue #Tiene basura
                    if x == "\n" : #BreakLine
                        if skip <= 0: #Saltar headers
                            #SAVE O HACER ALGO AQUI CON ESA LINE    
                            record = line.split("|")
                            if record[1] == "9999" or record[0] == "": break
                            ss = SorianaSerializer(data={
                                    "Fecha":Soriana.getFecha(record[0]),
                                    "Tienda":int(record[1]),
                                    "Donadores":int(record[2]),
                                    "Monto":float(record[3])})
                            if ss.is_valid():
                                ss.save()
                            else:
                                print(ss.errors)
                        else:
                            skip -= 1
                        line = ""
                        continue
                    line += x
                return Response({"msg":"OK"}, status = status.HTTP_201_CREATED)
        return Response({"msg":"WRONG FILE"}, status=status.HTTP_400_BAD_REQUEST)

#ViewSets
class BanamexViewSet(viewsets.ModelViewSet):
    serializer_class = BanamexSerializer
    queryset = Banamex.objects.all()

class SorianaViewSet(viewsets.ModelViewSet):
    serializer_class = SorianaSerializer
    queryset = Soriana.objects.all()
    