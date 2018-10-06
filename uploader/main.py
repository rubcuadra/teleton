from requests import post
from glob import glob

if __name__ == '__main__':
	url = "http://localhost:8000/api/v1/banamex/"
	folder = "2016/Banamex"

	for f in glob(f"{folder}/*.txt"):
		print(f)
		files = {'fisier': open(f,'rb')}
		r = post(url, files=files)
		print(r.text)