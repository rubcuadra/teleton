# -*- coding: utf-8 -*- 
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from codecs import EncodedFile, BOM_UTF8
from django.db.models import Sum
from bs4 import BeautifulSoup
from django.utils import timezone
from datetime import datetime
from random import randint
from datetime import timedelta  
import csv

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

class FarmaciasAhorroUploadViewSet(APIView):
    def post(self,request):
        if FILE_HEADER in request.FILES:
            f = request.FILES[FILE_HEADER]
            if f:
                skip = 1
                line = ""
                for x in f.read():
                    if x == '\x00' or x == "\r": continue #Tiene basura
                    if x == "\n" : #BreakLine
                        if skip <= 0: #Saltar headers
                            #SAVE O HACER ALGO AQUI CON ESA LINE    
                            record = line.split(",")

                            ss = FarmaciaAhorroSerializer(data={
                                    "Fecha": FarmaciaAhorro.getFecha(record[0]),
                                    "Tienda":int(record[1]),
                                    "suc_nombre":record[2].decode("ascii","ignore"),
                                    "region":record[3].decode("ascii","ignore"),
                                    "movements": int(record[5]),
                                    "Importe":float(record[6]),
                                    "Estado": Estado.FarmaciaAhorroParser( record[4] ) })
                            if ss.is_valid(): ss.save()
                            else:             print(ss.errors)
                        else:
                            skip -= 1
                        line = ""
                        continue
                    line += x
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
        pth = "%s://%s%s"%(request.scheme,request.META['HTTP_HOST'],request.path)
        ops    = [Banamex,FarmaciaAhorro,None,Soriana,None,None,Telmex]
        if src:
            model = ops[int(src)]
            a = model.objects.get_over_datetime(dt)
            c = a.count()
            toReturn = a[offset:offset+limit]
            nxt = "%s?time=%s&offset=%s&limit=%s&src=%s"%(pth,time,offset+limit,limit,src) if offset<c else None
            prv = "%s?time=%s&offset=%s&limit=%s&src=%s"%(pth,time,offset-limit,limit,src) if offset>0 else None
            return Response({"count":c,"next":nxt,"prev":prv,"data":[{"src":int(src),"amount":i.getAmount(),"datetime":i.Fecha,"location": EstadoSerializer(i.Estado).data } for i in toReturn]}) 
        else:
            c = sum( [a.objects.get_over_datetime(dt).count() for a in ops if a] )
            acum = 0
            for ix,model in enumerate(ops):
                if model:
                    a = model.objects.get_over_datetime(dt)
                    cc = a.count()
                    if acum+cc < offset: 
                        acum += cc
                        continue
                    else:
                        toReturn = a[offset-acum:offset-acum+limit]
                        nxt = "%s?time=%s&offset=%s&limit=%s"%(pth,time,acum+offset+limit,limit)
                        prv = "%s?time=%s&offset=%s&limit=%s"%(pth,time,acum+offset-limit,limit) if acum+offset-limit>0 else None
                        return Response({"count":c,"next":nxt,"prev":prv,"data":[{"src":randint(0,len(ops)), #ix
                            "amount":i.getAmount(),"datetime":i.Fecha,"location": EstadoSerializer(i.Estado).data } for i in toReturn]}) 
                
            prv = "%s?time=%s&offset=%s&limit=%s"%(pth,time,c-limit+1,limit) if c-limit+1>0 else None
            return Response({"count":c,"next":None,"prev":prv,"data":[]}) 
        return Response({"MSG":dt})


class TimeIntervalsViewSet(APIView):
    def get(self,request): #FIx acumulative data such as Telmex
        ops    = [Banamex,FarmaciaAhorro,None,Soriana,None,None,Telmex]
        interv = timedelta(minutes=60) #Interval
        toRet = {}
        for op in ops:
            if op:
                toRet[op.__name__] = []

                _min = op.objects.earliest().Fecha
                _max = op.objects.latest().Fecha

                print(_max - _min)

                temp = _min + interv
                c = op.objects.filter( Fecha__gte=_min , Fecha__lte=temp )
                toRet[op.__name__].append( (_min, op.SumAmount(c)  ) )
                ix = 0
                mx = float("-inf")
                while temp<_max:
                    _min = temp
                    temp = _min + interv
                    c = op.objects.filter( Fecha__gte=_min , Fecha__lte=temp )
                    
                    toRet[op.__name__].append( (_min, op.SumAmount(c)  ) )

                    if mx < toRet[op.__name__][-1][1]:
                        mx  = toRet[op.__name__][-1][1]
                        mxi = ix

                    ix+=1
                #MAX FOR THAT ONE 
                #print(mxi,mx,toRet[op.__name__][mxi])
        return Response(toRet)            

#Missing
class SourcesViewSet(APIView):
    def get(self,request):
        toRet = [{
            "id":0,
            "name":"Banamex",
            "total": Banamex.objects.all().count(),
            "amount": Banamex.objects.get_total_amount()
        },{
            "id":1,
            "name":"Farmacias del Ahorro",
            "total": FarmaciaAhorro.objects.all().count(),
            "amount": FarmaciaAhorro.objects.get_total_amount()
        },{
            "id":2,
            "name":"Infinitum",
            "total": 0,
            "amount": 0
        },{
            "id":3,
            "name":"Soriana",
            "total": Soriana.objects.all().count(),
            "amount": Soriana.objects.get_total_amount()
        },{
            "id":4,
            "name":"Telcel",
            "total": 11487,
            "amount": 2868700.00
        },{
            "id":5,
            "name":"Telecomm",
            "total": 35528,
            "amount": 912555.089
        },{
            "id":6,
            "name":"Telmex",
            "total": sum([n.Llamadas for n in Telmex.objects.filter(Fecha=Telmex.objects.latest().Fecha)]), #94898
            "amount": Telmex.objects.get_total_amount() #31042350 
        }]
        
        return Response(toRet)


#ViewSets
class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()

class FarmaciaAhorroViewSet(viewsets.ModelViewSet):
    serializer_class = FarmaciaAhorroSerializer
    queryset = FarmaciaAhorro.objects.all()

class BanamexViewSet(viewsets.ModelViewSet):
    serializer_class = BanamexSerializer
    queryset = Banamex.objects.all()

class SorianaViewSet(viewsets.ModelViewSet):
    serializer_class = SorianaSerializer
    queryset = Soriana.objects.all()

class CentrosViewSet(viewsets.ModelViewSet):
    serializer_class = CentrosSerializer
    queryset = Centros.objects.all()
    def list(self,request):
        r = []
        for crit in self.queryset:
            d = self.serializer_class(crit).data 
            d["current"] = Income.objects.filter(Centro_id=crit.id).aggregate(Sum('Monto'))["Monto__sum"]
            d["current"] = d["current"] if d["current"] else randint( int(d["required"]*0.2) , int(d["required"]*0.8) )
            r.append(d)
        return Response( {"results": r} )
    
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
    