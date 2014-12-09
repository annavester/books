from django.db import models

class ReadingList(models.Model):
    name =      models.CharField(max_length=50)
    dateadded = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name