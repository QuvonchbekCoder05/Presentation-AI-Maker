from rest_framework import serializers
from presentations.models.template import Template


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ["id", "name", "file"]
