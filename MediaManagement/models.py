from django.db import models

# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    alt = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    elclass = models.CharField(max_length=1500, null=True, blank=True)
    elid = models.CharField(max_length=255, null=True, blank=True)
    file = models.ImageField(upload_to='images')

    def __str__(self):
        title = ''
        if self.name is not None:
            title = self.name
        elif self.title is not None:
            title = self.title
        elif self.alt is not None:
            title = self.alt
        title += self.file
        return title