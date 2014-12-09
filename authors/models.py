from django.db import models

class Author(models.Model):   
    first_name =    models.CharField(max_length=60, null=True, blank=True)
    last_name =     models.CharField(max_length=60, null=True, blank=True)
    company_name =  models.CharField(max_length=100, null=True, blank=True)
    bio =           models.CharField(max_length=9000, null=True, blank=True)
    wiki =          models.CharField(max_length=450, null=True, blank=True)
    favorite =      models.BooleanField()
    website =       models.CharField(max_length=750, null=True, blank=True)