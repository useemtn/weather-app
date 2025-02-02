from django.db import models

class Pais(models.Model):
    """
    
    Tabla de paises
    
    """
    
    cca2 = models.CharField(max_length=2)
    cca3 = models.CharField(max_length=3)
    nombre = models.CharField(max_length=255)
    capital = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    subregion = models.CharField(max_length=255)
    miembroUE = models.BooleanField()
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Frontera(models.Model):
    """	
    
    Tabla de fronteras
    
    """
    idpais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    cca3_frontera = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.idpais.nombre} - {self.cca3_frontera}"

class Temperatura(models.Model):
    """
    
    Tabla de temperaturas
    
    """
    idpais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    temperatura = models.FloatField()
    sensacion = models.FloatField()
    minima = models.FloatField()
    maxima = models.FloatField()
    humedad = models.FloatField()
    amanecer = models.TimeField()
    atardecer = models.TimeField()

    def __str__(self):
        return f"{self.idpais.nombre} - {self.temperatura}°C"