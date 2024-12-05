from django.db import models


class Template(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="templates/")

    def __str__(self):
        return self.name
