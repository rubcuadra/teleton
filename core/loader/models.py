# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
# from channels import Group
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from datetime import datetime
# from django.contrib.auth import get_user_model
import json
from django.db.models import Sum
from collections import defaultdict

SORIANA_SUCURSALES_TO_STATE = {1:19,2:6,3:19,4:6,5:19,6:9,7:19,8:19,9:19,10:19,11:6,12:19,13:6,14:19,15:9,16:14,17:28,18:28,19:28,20:19,21:6,22:19,23:19,24:19,25:6,26:9,27:19,28:14,29:9,30:11,31:28,32:11,33:6,34:6,35:10,36:9,37:10,38:9,39:9,40:2,41:6,42:9,43:6,44:32,45:10,46:9,47:6,48:10,49:10,50:19,51:28,52:6,53:19,54:19,55:9,56:28,57:14,58:28,59:19,60:32,61:14,62:22,63:19,64:28,65:6,66:19,67:28,68:6,69:24,70:9,71:28,72:30,73:30,74:29,75:28,76:28,77:9,78:11,79:16,80:7,81:30,82:25,83:27,84:14,85:9,86:13,87:21,88:19,89:9,90:9,91:26,92:19,93:10,94:28,95:25,96:21,97:9,98:26,99:26,100:18,102:11,103:30,104:27,105:20,106:11,107:7,108:25,109:28,110:31,111:19,112:26,113:22,114:8,115:6,116:19,117:4,118:22,119:19,120:5,121:6,122:30,123:11,124:26,125:25,126:23,127:4,128:21,129:25,130:26,131:9,132:19,133:19,134:27,135:27,136:13,137:13,138:14,139:24,140:26,141:24,142:9,143:14,144:14,145:30,146:4,147:28,148:16,149:30,150:14,151:24,152:19,153:14,154:9,155:11,156:6,157:16,158:9,159:28,160:14,161:19,162:9,163:15,164:15,165:15,166:7,167:15,168:24,169:15,170:23,171:15,172:16,173:27,174:23,175:11,176:6,177:14,178:11,179:14,180:15,181:28,182:6,183:6,184:11,185:6,186:27,187:9,188:15,189:30,190:10,191:23,192:2,193:24,194:25,195:21,196:9,197:15,198:14,199:3,200:15,201:13,202:3,203:19,204:25,205:15,206:26,207:7,208:16,209:11,210:15,211:22,212:6,213:14,214:13,215:15,216:15,217:25,218:26,219:8,220:23,221:28,222:15,223:6,224:21,225:15,226:32,227:1,228:19,229:16,230:16,231:22,232:26,233:22,234:3,235:23,236:12,237:6,238:19,239:16,240:11,241:19,242:9,243:6,244:15,245:31,246:12,247:15,248:24,249:26,250:1,251:1,252:1,253:1,254:1,255:1,256:26,257:1,258:15,259:1,260:15,261:1,262:1,263:11,264:19,265:19,266:19,267:22,268:15,269:1,270:6,271:15,272:1,273:19,274:12,275:19,276:23,277:15,278:21,279:1,280:11,281:15,282:8,283:11,284:1,285:15,286:1,287:29,288:20,289:14,290:1,291:1,292:15,293:16,294:30,295:20,296:20,297:30,298:29,299:15,300:1,301:14,302:14,303:14,304:14,305:14,306:14,307:2,308:14,309:32,310:18,311:14,312:14,313:14,314:14,315:14,316:14,317:14,318:14,319:14,320:14,321:14,322:14,323:14,324:14,325:14,326:14,327:14,328:14,329:25,330:14,331:14,332:14,333:14,334:3,335:3,336:3,337:3,338:3,339:3,340:24,341:19,342:19,343:19,344:19,345:19,346:19,347:26,348:19,349:19,350:28,351:28,352:28,353:10,354:28,355:27,356:19,357:28,358:19,359:19,360:19,361:28,362:28,363:28,364:6,365:19,366:19,367:28,368:19,369:19,370:28,371:12,372:11,373:3,374:3,375:3,376:3,377:3,378:3,379:3,380:3,381:3,382:3,383:3,384:3,385:3,386:3,387:3,388:3,389:3,390:3,391:3,392:3,393:3,394:3,395:3,396:3,397:1,398:12,399:12,400:15,401:23,402:15,403:15,404:30,405:15,406:15,407:17,408:30,409:15,410:30,411:1,412:8,413:30,414:5,415:15,416:6,417:21,418:1,419:1,420:15,422:15,423:1,424:15,425:1,426:15,427:15,428:30,429:13,430:11,431:31,432:31,433:31,434:31,435:31,436:5,437:31,438:31,439:5,440:27,441:27,442:23,443:23,444:31,445:22,446:11,447:1,448:27,449:6,450:11,451:27,452:6,453:11,454:27,455:6,456:22,457:31,458:18,459:25,460:31,461:14,462:30,463:8,464:11,465:11,466:15,467:30,468:6,469:3,470:3,471:3,472:26,473:14,474:15,475:15,476:19,477:27,478:15,479:21,480:19,481:19,482:19,483:11,484:20,485:32,486:15,487:8,488:17,489:14,490:14,491:30,492:30,493:32,494:32,495:18,496:30,497:14,498:9,499:9,500:15,501:19,502:3,503:3,504:11,505:19,506:19,507:6,509:21,510:4,511:30,512:14,513:5,514:5,515:15,516:11,517:16,518:19,519:25,520:26,521:4,522:1,523:31,524:9,525:15,526:15,527:23,528:12,529:8,530:14,531:26,532:10,533:11,534:14,535:8,536:29,537:5,538:21,539:9,540:6,541:3,542:3,543:3,544:23,545:19,546:30,547:1,550:3,551:3,552:3,553:15,555:14,556:12,557:16,558:6,559:6,560:6,561:6,562:10,563:8,564:18,565:25,566:31,568:3,569:19,570:19,571:30,573:24,575:30,577:16,579:30,580:9,582:8,583:6,584:28,585:12,586:30,587:3,588:30,589:5,590:8,591:19,592:30,593:25,594:8,595:8,596:31,597:9,598:14,600:7,601:14,602:6,603:16,604:16,605:32,606:30,608:19,611:30,615:3,616:18,617:19,624:19,625:1,633:15,634:8,635:10,1001:6,1002:6,1003:9,1004:6,1005:13,1006:27,1007:19,1008:8,1009:7,1010:4,1011:28,1012:4,1013:28,1014:28,1015:10,1016:23,1017:15,1018:15,1019:10,1020:15,1021:19,1022:26,1023:25,1024:23,1025:4,1026:15,1027:15,1028:22,1029:19,1030:19,1031:21,1032:19,1033:6,5513:15,5514:15,5516:14,5519:3,5521:27,5525:3,5530:19,5558:14,5567:26,5578:22,5586:9,5589:15,5598:19,568:27}

class Estado(models.Model):
    """ DADOS POR INEGI
    1   DF
    2   Aguascalientes
    3   Baja California Norte
    4   Baja California Sur
    5   Campeche
    8   Chiapas
    9   Chihuahua
    6   Coahuila
    7   Colima
    10  Durango
    11  Estado de México 
    12  Guanajuato
    13  Guerrero
    14  Hidalgo
    15  Jalisco
    16  Michoacán
    17  Morelos
    18  Nayarit
    19  Nuevo León
    20  Oaxaca
    21  Puebla
    22  Querétaro
    23  Quintana Roo
    24  San Luis Potosí
    25  Sinaloa
    26  Sonora
    27  Tabasco
    28  Tamaulipas
    29  Tlaxcala
    30  Veracruz
    31  Yucatán
    32  Zacatecas
    """
    _id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30)
    lat = models.DecimalField(max_digits=12, decimal_places=8)
    lng = models.DecimalField(max_digits=12, decimal_places=8)
    
    @staticmethod
    def SorianaParser(estadoSoriana):
        SORIANA_PARSER = { 15:11,11:12, 12:13, 13:14,14:15}
        if estadoSoriana in SORIANA_PARSER: return int(SORIANA_PARSER[estadoSoriana]) 
        return int(estadoSoriana) #it is already ok

    @staticmethod
    def BanamexParser(estadoBanamex):
        BANAMEX_PARSER = { 1:2,2:3,3:4,4:5,7:8,8:9,5:6,6:7,9:1,15:11,11:12,12:13,13:14,14:15 }
        if estadoBanamex in BANAMEX_PARSER: return BANAMEX_PARSER[estadoBanamex]
        return int(estadoBanamex) #it is already ok
        
    @staticmethod
    def TelmexParser(estadoTelmex):
        return {
            "Aguascalientes":2,
            "Baja California Norte":3,
            "Baja California Sur":4,
            "Campeche":5,
            "Chiapas":8,
            "Chihuahua":9,
            "Coahuila":6,
            "Colima":7,
            "DF":1,
            "Durango":10,
            "Estado de Mxico":11,
            "Guanajuato":12,
            "Guerrero":13,
            "Hidalgo":14,
            "Jalisco":15,
            "Michoacn":16,
            "Morelos":17,
            "Nayarit":18,
            "Nuevo Len":19,
            "Oaxaca":20,
            "Puebla":21,
            "Quertaro":22,
            "Quintana Roo":23,
            "San Luis Potos":24,
            "Sinaloa":25,
            "Sonora":26,
            "Tabasco":27,
            "Tamaulipas":28,
            "Tlaxcala":29,
            "Veracruz":30,
            "Yucatn":31,
            "Zacatecas":32,
            "TOTALES":-1,
        }[estadoTelmex]

class BanamexManager(models.Manager):
    def get_over_datetime(self,dt): return self.filter(Fecha__gt=dt) #Newer
    def get_total_amount(self):     return self.aggregate(Sum('Monto'))["Monto__sum"]

class Banamex(models.Model):
    MEDIO_CHOICE = (\
        (1, 'Sucs'),
        (2, 'Cats'),
        (3, 'Corr'),
        (4, 'Bnet'),
        (5, 'Tfer'),
        (6, 'Alcancias'),
        (7, 'Otro 7'),
        (8, 'Otro 8'),
        (9, 'Otro 9'),
    )

    TIPO_CHOICE = (
        (1, 'Efec'),
        (2, 'ChBx'),
        (3, 'ChOB'),
        (4, 'TBNX'),
        (5, 'TOBS'),
        (6, 'AMEX'),
        (7, 'Otro 7'),
        (8, 'Otro 8'),
        (9, 'Otro 9'),
    )

    Fecha = models.DateTimeField(auto_now=False) #fecha y hora
    Medio = models.IntegerField(choices=MEDIO_CHOICE)
    Tipo = models.IntegerField(choices=TIPO_CHOICE)
    Sucursal = models.IntegerField()
    Cuenta = models.IntegerField()
    Autorizacion = models.BigIntegerField(primary_key=True) #12 digits, integer has 10
    Monto = models.DecimalField(max_digits=15, decimal_places=2)
    Estado = models.ForeignKey(Estado)
    objects = BanamexManager()

    def getAmount(self): return self.Monto
    
    @staticmethod
    def getFecha(fecha,hora): #aaaammdd, hhmm
        fecha = str(fecha)
        hora = str(hora)
        o = [ fecha[:4],fecha[4:6],fecha[6:],hora[:2],hora[2:] ]
        return datetime(*[int(k) for k in o])
    
class SorianaManager(models.Manager):
    def get_over_datetime(self,dt):
        return self.filter(Fecha__gt=dt) #Newer

    def get_total_amount(self): 
        return self.aggregate(Sum('Monto'))["Monto__sum"]
    
class Soriana(models.Model):
    Donadores = models.BigIntegerField() 
    Fecha = models.DateTimeField(auto_now=False) #fecha y hora
    Tienda = models.IntegerField()
    Monto = models.DecimalField(max_digits=16, decimal_places=8)
    Estado = models.ForeignKey(Estado)
    objects = SorianaManager()

    def getAmount(self): return self.Monto

    @staticmethod
    def getFecha(fecha): #aaaa-mm-dd hh:mmtt EJ. 20161211   2:00AM
        return datetime.strptime(fecha,"%Y%m%d   %I:%M%p")
        
    class Meta:
        unique_together = (("Fecha", "Tienda"),)

class TelmexManager(models.Manager):
    def get_over_datetime(self,dt):
        return self.filter(Fecha__gt=dt) #Newer

    def get_total_amount(self): 
        newest = self.filter(Fecha=self.latest().Fecha)
        return sum(n.Importe for n in newest)

class Telmex(models.Model):
    Fecha = models.DateTimeField(auto_now=False) #fecha y horaT
    Estado = models.ForeignKey(Estado)
    Llamadas = models.IntegerField()
    Importe = models.DecimalField(max_digits=13, decimal_places=3)
    Porcentaje = models.DecimalField(max_digits=8, decimal_places=4) #Por monto acumulado...wtf?
    objects = TelmexManager()

    def getAmount(self): return self.Importe
    class Meta:
        unique_together = (("Fecha", "Estado"),)
        get_latest_by = 'Fecha'

class Pacientes(models.Model):
    FL_PACIENTE = models.BigIntegerField() 
    NB_ALIAS = models.CharField(max_length=40,verbose_name='alias') 
    EDAD = models.CharField(max_length=10,verbose_name='edad')
    NB_ENFERMEDAD = models.CharField(max_length=255,verbose_name='enfermedad')
    #Egresos
    CL_ESTATUS = models.CharField(max_length=1,verbose_name='estatus', blank=True, null=True)
    DS_LOGROS = models.CharField(max_length=1000,verbose_name='logros', blank=True, null=True)
    DS_TESTIMONIO = models.CharField(max_length=1000,verbose_name='testimonios', blank=True, null=True)

class Centros(models.Model):
    name = models.CharField(max_length=50) 
    required = models.BigIntegerField(verbose_name='Recursos necesarios 2018')
    promised = models.BigIntegerField(verbose_name='Ingresos comprometidos')
    estimated_accomplishment = models.IntegerField(verbose_name='\% esperado de cumplimiento')
    estimated = models.BigIntegerField(verbose_name='Ingresos esperados')
    required_event = models.BigIntegerField(verbose_name='Recursos necesarios en evento Teleton')
    capacity = models.IntegerField(verbose_name='Capacidad de pacientes')
    anual_cost = models.IntegerField(verbose_name='Costo anual promedio por paciente')
    amount_help = models.IntegerField(verbose_name='Numero de pacientes por cubrir con donativos')
    lat = models.DecimalField(max_digits=12, decimal_places=8,default=0.0)
    lng = models.DecimalField(max_digits=12, decimal_places=8,default=0.0)
