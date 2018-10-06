# -*- coding: utf-8 -*- 
# from loader.models import *
from loader.serializers import *
from loader.models import *
from codecs import EncodedFile
import csv

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