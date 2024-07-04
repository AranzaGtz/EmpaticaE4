from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()

#   MODELO PARA ANALIZAR TEMPERATURA
class AnalisisTemperatura(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    promedio = models.FloatField()
    mediana = models.FloatField()
    maximo = models.FloatField()
    minimo = models.FloatField()
    inicio_sesion = models.DateTimeField(null=True, blank=True)
    tasa_muestreo = models.FloatField(null=True, blank=True)


#   MODELO PARA ANALIZAR FRECUANCIA CARDIACA
class AnalisisFrecuenciaCardiaca(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    promedio = models.FloatField()
    mediana = models.FloatField()
    maximo = models.FloatField()
    minimo = models.FloatField()
    inicio_sesion = models.DateTimeField(null=True, blank=True)
    tasa_muestreo = models.FloatField(null=True, blank=True)