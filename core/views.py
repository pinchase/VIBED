from rest_framework import viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Client, Testimonial, Brand, BrandImage
from .serializers import (
    TestimonialSerializer,
)


# ============ API VIEWS ============

# class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Project.objects.all()
#     lookup_field = 'slug'
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter,
#     ]
#     search_fields = ['title', 'brand__name', 'brand__client__name']
#     ordering_fields = ['created_at', 'featured']
#     ordering = ['-created_at']
#     filterset_fields = ['featured', 'brand__client']

#     def get_serializer_class(self):
#         """Use lightweight serializer for list view, detailed for retrieve."""
#         if self.action == 'retrieve':
#             return ProjectDetailSerializer
#         return ProjectListSerializer


class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']


# ============ TEMPLATE VIEWS ============

class HomePageView(View):
    """Homepage with clients, testimonials, and route-to-market positioning."""
    
    def get(self, request):
        testimonials = Testimonial.objects.all()[:3]
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
        brand = get_object_or_404(Brand, slug=slug, is_active=True, client__is_active=True)
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


class CaseStudiesListView(View):
    """Case studies listing with pagination and search"""
    
    def get(self, request):
        projects = Project.objects.all()
        search_query = request.GET.get('search', '')
        featured_only = request.GET.get('featured', '')
        
        if search_query:
            projects = projects.filter(
                title__icontains=search_query
            ) | projects.filter(
                brand__name__icontains=search_query
            ) | projects.filter(
                brand__client__name__icontains=search_query
            )
        
        if featured_only == 'on':
            projects = projects.filter(featured=True)
        
        paginator = Paginator(projects, 9)
        page = request.GET.get('page')
        
        try:
            projects_page = paginator.page(page)
        except PageNotAnInteger:
            projects_page = paginator.page(1)
        except EmptyPage:
            projects_page = paginator.page(paginator.num_pages)
        
        context = {
            'projects': projects_page,
            'search_query': search_query,
            'featured_only': featured_only,
            'page_title': 'Case Studies - Braymell',
        }
        return render(request, 'core/case-studies.html', context)


class CaseStudyDetailView(View):
    """Single case study detail page"""
    
    def get(self, request, slug):
        project = get_object_or_404(Project, slug=slug)
        images = project.images.all()
        related_projects = Project.objects.exclude(slug=slug).all()[:3]
        
        context = {
            'project': project,
            'images': images,
            'related_projects': related_projects,
            'page_title': f'{project.title} - Braymell',
        }
        return render(request, 'core/case-study-detail.html', context)


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
