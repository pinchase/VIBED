
# URL configuration for config project.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_spectacular.views import SpectacularRedocView
from core.views import (
    HomePageView,
    ClientsListView,
    ClientDetailView,
    BrandDetailView,
    TestimonialsPageView,
    AboutPageView,
    ContactPageView,
)


template_patterns = [
    path('', HomePageView.as_view(), name='home'),
    path('clients/', ClientsListView.as_view(), name='clients'),
    path('clients/<slug:slug>/', ClientDetailView.as_view(), name='client-detail'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand-detail'),
    path('testimonials/', TestimonialsPageView.as_view(), name='testimonials'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
]

# API Documentation
api_docs = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.urls')),
] + template_patterns + api_docs

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
