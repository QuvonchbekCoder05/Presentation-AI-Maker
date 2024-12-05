from django.db import models


class Presentation(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slides_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey("Template", on_delete=models.CASCADE)

    def __str__(self):
        return self.title
