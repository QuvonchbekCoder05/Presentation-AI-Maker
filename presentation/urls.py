from django.urls import path
from presentations.views import PresentationView

urlpatterns = [
    path("presentations/", PresentationView.as_view(), name="presentations"),
]
