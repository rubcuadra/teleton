# -*- coding: utf-8 -*- 
from loader.models import *
from loader.serializers import *
# from codecs import EncodedFile
# from request import post
# import csv

# BANAMEX_PARSER = { 1:2,2:3,3:4,4:5,7:8,8:9,5:6,6:7,9:1,15:11,11:12,12:13,13:14,14:15 }
# for key, value in BANAMEX_PARSER.iteritems(): Banamex.objects.filter(Estado=key).update(Estado=value)

# with open("kids.csv", "r") as f:
# 	data = csv.DictReader( f , delimiter=";")
# 	for row in data:
# 		ps = PacientesSerializer(data = row)
# 		try:
# 			if ps.is_valid():
# 				ps.save()
# 			else:
# 				print(ps.errors)
# 		except:
# 			pass

# with open("crits.csv", "r") as f:
# 	data = csv.DictReader( EncodedFile(f, 'utf8', "utf-8-sig") , delimiter=";")
# 	for row in data:
# 		e = {
# 			"name":row["DESCRIPCION"],
# 		    "required":int(row["RN2018"].replace(" ", "")),
# 		    "promised":int(row["IC"].replace(" ", "")),
# 		    "estimated_accomplishment": int(row["EC"].strip("%")),
# 		    "estimated":int(row["IE"].replace(" ", "")),
# 		    "required_event":int(row["RNET"].replace(" ", "")),
# 			"capacity" : int(row["CN"].replace(" ", "")),
# 		    "anual_cost" : int(row["CAPP"].replace(" ", "")),
# 		    "amount_help" :int(row["NCD"].replace(" ", ""))
# 		}
		
# 		c = Centros(**e)
# 		c.save()

# states = [
# {"_id":2,	"name":"Aguascalientes","lat":21.85	,"lng":-102.3},
# {"_id":3,	"name":"Baja California Norte","lat":32.525	,"lng":-117.033333},
# {"_id":4,	"name":"Baja California Sur","lat":24.142222	,"lng":-110.310833},
# {"_id":5,	"name":"Campeche","lat":19.85	,"lng":-90.530556},
# {"_id":8,	"name":"Chiapas","lat":16.752778	,"lng":-93.116667},
# {"_id":9,	"name":"Chihuahua","lat":31.738581	,"lng":-106.487014},
# {"_id":6,	"name":"Coahuila","lat":25.433333	,"lng":-101.00},
# {"_id":7,	"name":"Colima","lat":19.052222	,"lng":-104.315833},
# {"_id":1,	"name":"DF","lat":19.3906797	,"lng":-99.2840407},
# {"_id":10,	"name":"Durango","lat":24.016667	,"lng":-104.666667},
# {"_id":11,	"name":"Estado de México","lat":19.609722	,"lng":-99.06},
# {"_id":12,	"name":"Guanajuato","lat":21.116667	,"lng":-101.683333},
# {"_id":13,	"name":"Guerrero","lat":16.863611	,"lng":-99.8825},
# {"_id":14,	"name":"Hidalgo","lat":20.1	,"lng":-98.75},
# {"_id":15,	"name":"Jalisco","lat":20.676667	,"lng":-103.3475},
# {"_id":16,	"name":"Michoacán","lat":19.768333	,"lng":-101.189444},
# {"_id":17,	"name":"Morelos","lat":18.918611	,"lng":-99.234167},
# {"_id":18,	"name":"Nayarit","lat":21.508333	,"lng":-104.893056},
# {"_id":19,	"name":"Nuevo León","lat":25.666667	,"lng":-100.3},
# {"_id":20,	"name":"Oaxaca","lat":17.067778	,"lng":-96.72},
# {"_id":21,	"name":"Puebla","lat":19.033333	,"lng":-98.183333},
# {"_id":22,	"name":"Querétaro","lat":20.5875	,"lng":-100.392778},
# {"_id":23,	"name":"Quintana Roo","lat":21.160556	,"lng":-86.8475},
# {"_id":24,	"name":"San Luis Potosí","lat":22.151111	,"lng":-100.976111},
# {"_id":25,	"name":"Sinaloa","lat":24.8	,"lng":-107.383333},
# {"_id":26,	"name":"Sonora","lat":29.098889	,"lng":-110.954167},
# {"_id":27,	"name":"Tabasco","lat":17.989167	,"lng":-92.928056},
# {"_id":28,	"name":"Tamaulipas","lat":26.092222	,"lng":-98.277778},
# {"_id":29,	"name":"Tlaxcala","lat":19.119	,"lng":-98.17},
# {"_id":30,	"name":"Veracruz","lat":19.190278	,"lng":-96.153333},
# {"_id":31,	"name":"Yucatán","lat":20.97	,"lng":-89.62},
# {"_id":32,	"name":"Zacatecas","lat":22.773611	,"lng":-102.573611}]
		
		
		