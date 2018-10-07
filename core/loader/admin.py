from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Centros)
class CentrosAdmin(admin.ModelAdmin):
    # inlines = (UserStoreInLine,)
    pass