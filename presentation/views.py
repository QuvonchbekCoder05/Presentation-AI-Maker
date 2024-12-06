from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from presentation.models.presentation import Presentation
from presentation.models.template import Template
from presentation.models.slide import Slide
from presentation.serializers.presentation_serializer import PresentationSerializer
from presentation.serializers.template_serializer import TemplateSerializer
from presentation.serializers.slide_serializer import SlideSerializer
from presentation.services.ai_content_generator import AIContentGenerator
from presentation.services.pptx_handler import PPTXHandler
from presentation.services.chart_generator import ChartGenerator
from presentation.services.image_generator import ImageGenerator


class TemplateListAPIView(APIView):
    """
    Barcha mavjud shablonlarni ro'yxatini qaytaruvchi API yaratib oldik.
    """
    def get(self, request):
        templates = Template.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)


class PresentationListCreateAPIView(APIView):
    """
    Prezentatsiyalarni yaratish va ro'yxatlash uchun API yaratib oldik.
    """
    def get(self, request):
        """
        Mavjud barcha prezentatsiyalarni qaytaradi.
        """
        presentations = Presentation.objects.all()
        serializer = PresentationSerializer(presentations, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Yangi prezentatsiya yaratadib olamiz .
        """
        serializer = PresentationSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get("title")  # Foydalanuvchi kiritgan mavzu
            slides_count = serializer.validated_data.get("slides_count", 20)  # Default qiymati 20 slayd
            template_id = serializer.validated_data.get("template_id")  # Tanlangan shablon IDsini validatsiua qilamiz

            if slides_count > 20:
                return Response(
                    {"error": "Slides count cannot exceed 20."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Shablonni olish qismi
            try:
                template = Template.objects.get(id=template_id)
            except Template.DoesNotExist:
                return Response(
                    {"error": "Template not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # **1. AI yordamida kontent generatsiyasi**
            ai_generator = AIContentGenerator()
            content = ai_generator.generate_content(title, slides_count)

            # **2. Rasmlar generatsiyasi**
            image_generator = ImageGenerator()
            images = image_generator.generate_images(content)

            # **3. Diagrammalar generatsiyasi**
            chart_generator = ChartGenerator()
            charts = chart_generator.generate_charts(content)

            # **4. Slaydlarni yaratish**
            slides = []
            for slide_content, slide_image, slide_chart in zip(content, images, charts):
                slide = Slide.objects.create(
                    content=slide_content,
                    image=slide_image,
                    chart=slide_chart,
                )
                slides.append(slide)

            # **5. PowerPoint faylini yaratish**
            pptx_handler = PPTXHandler()
            pptx_path = pptx_handler.create_presentation(slides, template)

            # **6. Prezentatsiyani saqlash**
            presentation = serializer.save(pptx_path=pptx_path)

            return Response(
                {
                    "detail": "Presentation created successfully.",
                    "pptx_url": request.build_absolute_uri(pptx_path),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)