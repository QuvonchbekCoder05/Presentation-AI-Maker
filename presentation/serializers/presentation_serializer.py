from rest_framework import serializers
from presentations.models.presentation import Presentation
from presentations.models.slide import Slide


class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ["id", "title", "content", "image_url"]


class PresentationSerializer(serializers.ModelSerializer):
    slides = SlideSerializer(many=True, read_only=True)

    class Meta:
        model = Presentation
        fields = ["id", "title", "description", "slides_count", "slides", "created_at"]
