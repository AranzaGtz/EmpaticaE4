from django.contrib import admin
from .models import (AnalisisTemperatura, AnalisisFrecuenciaCardiaca, Usuario,
                     AnalisisAcelerometro, AnalisisBVP, AnalisisIBI)

# Register your models here.
admin.site.register(AnalisisTemperatura)
admin.site.register(AnalisisFrecuenciaCardiaca)
admin.site.register(AnalisisAcelerometro)
admin.site.register(AnalisisBVP)
admin.site.register(AnalisisIBI)
admin.site.register(Usuario)
