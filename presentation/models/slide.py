from django.db import models


class Slide(models.Model):
    presentation = models.ForeignKey(
        "Presentation", on_delete=models.CASCADE, related_name="slides"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
