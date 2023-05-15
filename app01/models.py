from django.db import models

# Create your models here.
class NavBar(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    parent_id = models.IntegerField(blank=True, null=True)
    sort = models.IntegerField()
