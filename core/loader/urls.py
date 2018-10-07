from django.conf.urls import url, include
from .views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'banamex', BanamexViewSet,"Banamex")
router.register(r'soriana', SorianaViewSet,"Soriana")
router.register(r'centros', CentrosViewSet,"Centros")
router.register(r'pacientes', PacientesViewSet,"Pacientes")
router.register(r'estados', EstadoViewSet,"Estados")
router.register(r'telmex', TelmexViewSet,"Telmex")
router.register(r'fahorro', FarmaciaAhorroViewSet,"FarmaciaAhorro")

urlpatterns = [
	url(r'^', include(router.urls), name='Loader'), 
	url(r'^upload/banamex/', BanamexUploadViewSet.as_view(), name='upload_banamex'),
	url(r'^upload/soriana/', SorianaUploadViewSet.as_view(), name='upload_soriana'),
	url(r'^upload/telmex/', TelmexUploadViewSet.as_view(), name='upload_telmex'),
	url(r'^upload/fahorro/', FarmaciasAhorroUploadViewSet.as_view(), name='upload_fahorro'),
	url(r'^sources/', SourcesViewSet.as_view(), name='sources'),
	url(r'^map/', MapViewSet.as_view(), name='map'),
]