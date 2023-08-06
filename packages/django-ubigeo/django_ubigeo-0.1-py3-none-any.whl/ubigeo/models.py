from django.db import models

# Create your models here.

class UBIGEO_INEI(models.Model):
   cod_dep = models.CharField(max_length=2)
   desc_dep = models.CharField(max_length=13)
   cod_prov = models.CharField(max_length=4)
   desc_prov = models.CharField(max_length=25)
   cod_ubigeo = models.CharField(max_length=6, primary_key=True)
   desc_ubigeo = models.CharField(max_length=36)

class UBIGEO_RENIEC(models.Model):
   cod_dep = models.CharField(max_length=2)
   desc_dep = models.CharField(max_length=23)
   cod_prov = models.CharField(max_length=4)
   desc_prov = models.CharField(max_length=25)
   cod_ubigeo = models.CharField(max_length=6, primary_key=True)
   desc_ubigeo = models.CharField(max_length=30)

class UBIGEO_SUNAT(models.Model):
   cod_dep = models.CharField(max_length=2)
   desc_dep = models.CharField(max_length=23)
   cod_prov = models.CharField(max_length=4)
   desc_prov = models.CharField(max_length=25)
   cod_ubigeo = models.CharField(max_length=6, primary_key=True)
   desc_ubigeo = models.CharField(max_length=36)

