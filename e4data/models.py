from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()

class AnalisisBase(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    promedio = models.FloatField()
    mediana = models.FloatField()
    maximo = models.FloatField()
    minimo = models.FloatField()
    inicio_sesion = models.DateTimeField(null=True, blank=True)
    tasa_muestreo = models.FloatField(null=True, blank=True)

    class Meta:
        abstract = True

class AnalisisTemperatura(AnalisisBase):
    pass

class AnalisisFrecuenciaCardiaca(AnalisisBase):
    pass

class AnalisisAcelerometro(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    promedio_x = models.FloatField()
    promedio_y = models.FloatField()
    promedio_z = models.FloatField()
    mediana_x = models.FloatField()
    mediana_y = models.FloatField()
    mediana_z = models.FloatField()
    maximo_x = models.FloatField()
    maximo_y = models.FloatField()
    maximo_z = models.FloatField()
    minimo_x = models.FloatField()
    minimo_y = models.FloatField()
    minimo_z = models.FloatField()
    inicio_sesion = models.DateTimeField(null=True, blank=True)
    tasa_muestreo = models.FloatField(null=True, blank=True)

class AnalisisBVP(AnalisisBase):
    pass

class AnalisisIBI(AnalisisBase):
    pass

class AnalisisEDA(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    promedio = models.FloatField()
    mediana = models.FloatField()
    maximo = models.FloatField()
    minimo = models.FloatField()
    inicio_sesion = models.DateTimeField(null=True, blank=True)
    tasa_muestreo = models.FloatField(null=True, blank=True)
