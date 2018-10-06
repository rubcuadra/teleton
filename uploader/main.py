from requests import post
from glob import glob

if __name__ == '__main__':
	url = "http://localhost:8000/api/v1/banamex/"
	folder = "2016/Banamex"

	for f in glob(f"{folder}/*.txt"):
		files = {'fisier': open(f,'rb')}
		r = post(url, files=None)
		if r.status_code > 399:
			print(f)
