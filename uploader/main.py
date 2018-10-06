# -*- coding: utf-8 -*- 
from requests import post
from glob import glob

if __name__ == '__main__':
	current = "Banamex"
	
	url = f"http://localhost:8000/api/v1/upload/{current.lower()}/"
	folder = f"2016/{current}"

	for f in glob(f"{folder}/*.txt"):
		files = {'fisier': open(f,'rb')}
		r = post(url, files=files)
		print(f,r.status_code)
		