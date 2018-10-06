from rest_framework import permissions, viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import *
from codecs import EncodedFile, BOM_UTF8
import csv

class BanamexViewSet(APIView):
    def fix(self,row):
        row["Fecha"] = Banamex.getFecha(row["Fecha"],row["Hora"])
        del row["Hora"] #Useless
        return row

    def post(self,request):
        if "fisiser" in request.FILES:
            f = request.FILES["fisier"]
            if f:
                data = csv.DictReader( EncodedFile(f, 'utf8', "utf-8-sig") )
                bs = BanamexSerializer(data=[self.fix(d) for d in data],many=True)
                if bs.is_valid():
                    bs.save()
                    return Response({"msg":"OK"}, status = status.HTTP_201_CREATED)
                else:
                    return Response(bs.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"WRONG FILE"}, status=status.HTTP_400_BAD_REQUEST)

