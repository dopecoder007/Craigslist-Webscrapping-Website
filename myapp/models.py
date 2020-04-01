from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        verbose_name_plural = "Searches"

    # Here this function returns the value for the given field 
    def __str__(self):
        return '{}'.format(self.search)