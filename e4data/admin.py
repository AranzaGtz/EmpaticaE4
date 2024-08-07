from django.contrib import admin
from .models import (AnalisisTemperatura, AnalisisFrecuenciaCardiaca, 
                     AnalisisAcelerometro, AnalisisBVP, AnalisisIBI, 
                     AnalisisEDA, Usuario)

admin.site.register(AnalisisTemperatura)
admin.site.register(AnalisisFrecuenciaCardiaca)
admin.site.register(AnalisisAcelerometro)
admin.site.register(AnalisisBVP)
admin.site.register(AnalisisIBI)
admin.site.register(AnalisisEDA)
admin.site.register(Usuario)
