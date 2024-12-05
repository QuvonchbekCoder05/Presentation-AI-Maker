from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from presentations.models.presentation import Presentation
from presentations.models.template import Template
from presentations.models.slide import Slide
from presentations.serializers.presentation_serializer import PresentationSerializer
from presentations.serializers.template_serializer import TemplateSerializer
from presentations.serializers.slide_serializer import SlideSerializer
from presentations.services.ai_content_generator import generate_presentation_content
from presentations.services.pptx_handler import create_presentation_pptx
from presentations.services.chart_generator import generate_chart
from presentations.services.template_manager import get_template_by_id
from presentations.services.image_generator import generate_image


class PresentationView(APIView):
    def post(self, request):
        data = request.data
        title = data.get("title")
        slides_count = int(data.get("slides_count", 5))
        template_id = data.get("template_id")

        template = get_template_by_id(template_id)
        if not template:
            return Response(
                {"error": "Template not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # AI orqali kontent yaratish qismi
        slides_content = generate_presentation_content(title, slides_count)

        # Prezentatsiya yaratish qismi
        presentation = Presentation.objects.create(
            title=title,
            slides_count=slides_count,
            template=template,
        )

        # Har bir slaydni saqlash
        for slide in slides_content:
            image_url = None
            if slide.get("generate_image"):
                image_url = generate_image(slide["content"])

            Slide.objects.create(
                presentation=presentation,
                title=slide["title"],
                content=slide["content"],
                image_url=image_url,
            )

        # PowerPoint yaratiladi
        pptx_path = create_presentation_pptx(presentation)

        return Response(
            {"message": "Presentation created", "pptx_path": pptx_path},
            status=status.HTTP_201_CREATED,
        )
