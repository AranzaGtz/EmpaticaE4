from django.db import models

# Modelo para analisar Temperatura
class AnalisisTemperatura(models.Model):
    promedio = models.FloatField()
    mediana = models.FloatField()
    maximo = models.FloatField()
    minimo = models.FloatField()
    fecha_analisis = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Análisis de {self.fecha_analisis}"