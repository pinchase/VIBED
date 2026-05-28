from django.urls import path
from .views import (
    TestimonialListView,
)

# API endpoints
urlpatterns = [
    path('testimonials/', TestimonialListView.as_view(), name='testimonial-list'),
]
