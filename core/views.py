from rest_framework import generics, filters
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Client, Testimonial, Brand, BrandImage
from .serializers import (
    TestimonialSerializer,
)


class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']


# ============ TEMPLATE VIEWS ============

class HomePageView(View):
    """Homepage with clients, testimonials, and route-to-market positioning."""
    
    def get(self, request):
        testimonials = Testimonial.objects.filter(featured=True).order_by('-created_at')[:3]
        clients = Client.objects.filter(is_active=True).order_by('name')
        
        context = {
            'testimonials': testimonials,
            'clients': clients,
            'page_title': 'Home - Braymell',
        }
        return render(request, 'core/index.html', context)


class ClientsListView(View):
    """Public clients page with logos and company captions."""

    def get(self, request):
        clients = Client.objects.filter(is_active=True).order_by('name')

        context = {
            'clients': clients,
            'page_title': 'Clients - Braymell',
        }
        return render(request, 'core/clients.html', context)


class ClientDetailView(View):
    """Client-level work story with its brand portfolio."""

    def get(self, request, slug):
        client = get_object_or_404(Client, slug=slug, is_active=True)
        brands = client.brands.filter(is_active=True).order_by('order', 'name')
        other_clients = Client.objects.filter(is_active=True).exclude(pk=client.pk).order_by('name')[:6]

        context = {
            'client': client,
            'brands': brands,
            'other_clients': other_clients,
            'page_title': f'{client.name} - Braymell Client',
        }
        return render(request, 'core/client-detail.html', context)


class BrandDetailView(View):
    """Brand-level work page with narrative and image gallery."""

    def get(self, request, slug):
        brand = get_object_or_404(
            Brand.objects.select_related('client'),
            slug=slug,
            is_active=True,
            client__is_active=True,
        )
        images = BrandImage.objects.filter(brand=brand)
        programs = brand.programs.filter(is_active=True).order_by('order', 'title')
        related_brands = brand.client.brands.filter(is_active=True).exclude(pk=brand.pk).order_by('order', 'name')

        context = {
            'brand': brand,
            'images': images,
            'programs': programs,
            'related_brands': related_brands,
            'page_title': f'{brand.name} - Braymell Brand Work',
        }
        return render(request, 'core/brand-detail.html', context)


class TestimonialsPageView(View):
    """Testimonials listing page"""
    
    def get(self, request):
        testimonials = Testimonial.objects.all()
        paginator = Paginator(testimonials, 12)
        page = request.GET.get('page')
        
        try:
            testimonials_page = paginator.page(page)
        except PageNotAnInteger:
            testimonials_page = paginator.page(1)
        except EmptyPage:
            testimonials_page = paginator.page(paginator.num_pages)
        
        context = {
            'testimonials': testimonials_page,
            'page_title': 'Testimonials - Braymell',
        }
        return render(request, 'core/testimonials.html', context)


class AboutPageView(View):
    """About page"""
    
    def get(self, request):
        context = {
            'page_title': 'About - Braymell',
        }
        return render(request, 'core/about.html', context)


class ContactPageView(View):
    """Contact page"""
    
    def get(self, request):
        context = {
            'page_title': 'Contact - Braymell',
        }
        return render(request, 'core/contact.html', context)
