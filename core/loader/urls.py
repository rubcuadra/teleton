from django.conf.urls import url, include
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'banamex', BanamexViewSet,"Banamex")
router.register(r'soriana', SorianaViewSet,"Soriana")

urlpatterns = [
	url(r'^', include(router.urls), name='Loader'), 
	url(r'^upload/banamex/', BanamexUploadViewSet.as_view(), name='upload_banamex'),
	url(r'^upload/soriana/', SorianaUploadViewSet.as_view(), name='upload_soriana')
]