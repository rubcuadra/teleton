from django.conf.urls import url, include
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'Banamex', BanamexViewSet,"Banamex")

urlpatterns = [
	url(r'^banamex/', BanamexViewSet.as_view(), name='banamex')
	# url(r'^', include(router.urls), name='Loader'), 
]