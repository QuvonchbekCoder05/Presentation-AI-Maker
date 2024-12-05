from rest_framework import serializers
from presentations.models.slide import Slide


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ["id", "title", "content", "image_url"]
