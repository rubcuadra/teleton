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
from bs4 import BeautifulSoup
from django.utils import timezone
from datetime import datetime

FILE_HEADER = "fisier"

class BanamexUploadViewSet(APIView):
    def fix(self,row):
        row["Fecha"] = Banamex.getFecha(row["Fecha"],row["Hora"])
        row["Monto"] = row["Monto"]/100
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


class TelmexUploadViewSet(APIView):
    def post(self,request):
        if FILE_HEADER in request.FILES:
            f = request.FILES[FILE_HEADER]
            if f:
                try:    t = datetime.strptime(f.name, "Telmex_AcumEdo_%m%d%Y_%H%M.xls")
                except: return Response({"msg":"WRONG FILE NAME"}, status=status.HTTP_400_BAD_REQUEST)    
                doc = BeautifulSoup(f.read(), features="lxml")
                skip = 1
                for row in doc.find_all('tr'):
                    if skip > 0:
                        skip -= 1
                        continue
                    cells = row.find_all("td")

                    estado = Estado.TelmexParser(cells[0].get_text().encode("ascii","ignore").strip())
                    if estado == -1: break
                    
                    ts = TelmexSerializer(data={
                        "Fecha": t,
                        "Estado": estado,
                        "Llamadas": int(cells[1].get_text()),
                        "Importe": float(cells[2].get_text().strip("$").replace(",","")),
                        "Porcentaje": float(cells[3].get_text().strip("%"))
                    })
                    if ts.is_valid(): ts.save()
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
                                    "Monto":float(record[3]),
                                    "Estado":Estado.SorianaParser( SORIANA_SUCURSALES_TO_STATE.get(o.Tienda,1) ) })
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

class MapViewSet(APIView):
    def get(self,request):
        src = self.request.query_params.get("src")
        time = self.request.query_params.get("time")
        offset = int(self.request.query_params.get("offset",0))
        limit = int(self.request.query_params.get("limit",500))
        if not time: return Response({"msg":"WRONG PARAMS, must send time"}, status=status.HTTP_400_BAD_REQUEST)
        dt = timezone.make_aware( datetime.fromtimestamp(int( time )) , timezone.utc) 
        ops    = [Banamex,None,None,Soriana,None,None,Telmex]
        opsSer = [BanamexSerializer,None,None,SorianaSerializer,None,None,TelmexSerializer]
        if src:
            model, serializer = ops[int(src)], opsSer[int(src)]
            a = model.objects.get_over_datetime(dt)
            c = a.count()
            toReturn = a[offset:offset+limit]
            ser = serializer(toReturn,many=True)
            pth = "%s://%s%s"%(request.scheme,request.META['HTTP_HOST'],request.path)
            nxt = "%s?time=%s&offset=%s&limit=%s&src=%s"%(pth,time,offset+limit,limit,src) if offset<c else None
            prv = "%s?time=%s&offset=%s&limit=%s&src=%s"%(pth,time,offset-limit,limit,src) if offset>0 else None
            return Response({"count":c,"next":nxt,"prev":prv,"data":ser.data})
        else:
            acum = 0
            for i in range(0,len(ops)):
                model, serializer = ops[i], opsSer[i]
                if model:
                    a = model.objects.get_over_datetime(dt)
                    c = a.count()
                    if  acum + offset < c: #Go all here
                        toReturn = a[acum+offset:acum+offset+limit]
                        ser = serializer(toReturn,many=True)
                        pth = "%s://%s%s"%(request.scheme,request.META['HTTP_HOST'],request.path)
                        nxt = "%s?time=%s&offset=%s&limit=%s"%(pth,time,offset+limit,limit,src) if offset<c else None
                        prv = "%s?time=%s&offset=%s&limit=%ss"%(pth,time,offset-limit,limit,src) if offset>0 else None
                        return Response({"count":c,"next":nxt,"prev":prv,"data":ser.data})
                    else:
                        acum += offset

            return return Response({"count":c,"next":nxt,"prev":prv,"data":ser.data})

        return Response({"MSG":dt})

class SourcesViewSet(APIView):
    def get(self,request):
        toRet = [{
            "id":0,
            "name":"Banamex",
            "amount": Banamex.objects.get_total_amount()
        },{
            "id":1,
            "name":"Farmacias del Ahorro",
            "amount": 0
        },{
            "id":2,
            "name":"Infinitum",
            "amount": 0
        },{
            "id":3,
            "name":"Soriana",
            "amount": Soriana.objects.get_total_amount()
        },{
            "id":4,
            "name":"Telcel",
            "amount": 0
        },{
            "id":5,
            "name":"Telecomm",
            "amount": 0
        },{
            "id":6,
            "name":"Telmex",
            "amount": Telmex.objects.get_total_amount()
        }]
        
        return Response(toRet)

#ViewSets
class BanamexViewSet(viewsets.ModelViewSet):
    serializer_class = BanamexSerializer
    queryset = Banamex.objects.all()

class SorianaViewSet(viewsets.ModelViewSet):
    serializer_class = SorianaSerializer
    queryset = Soriana.objects.all()

class CentrosViewSet(viewsets.ModelViewSet):
    serializer_class = CentrosSerializer
    queryset = Centros.objects.all()
    
class PacientesViewSet(viewsets.ModelViewSet):
    serializer_class = PacientesSerializer
    queryset = Pacientes.objects.all()
    filter_fields = ("CL_ESTATUS",)

class EstadoViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoSerializer
    queryset = Estado.objects.all()

class TelmexViewSet(viewsets.ModelViewSet):
    serializer_class = TelmexSerializer
    queryset = Telmex.objects.all()
    