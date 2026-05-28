from django.contrib import admin
from .models import Client, Brand, BrandProgram, BrandImage, Testimonial
from django.utils.html import format_html

admin.site.site_header = "Braymells Admin Portal"
admin.site.site_title = "Braymells Dashboard"
admin.site.index_title = "Welcome to Braymells Administration"


class ActiveStatusAdminMixin:
    actions = ['mark_active', 'mark_inactive']

    @admin.action(description="Mark selected as active")
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Mark selected as inactive")
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)


class BrandInline(admin.TabularInline):
    model = Brand
    extra = 1
    fields = ['name', 'logo', 'caption', 'order', 'is_active']
    ordering = ['order']

    
@admin.register(Client)
class ClientAdmin(ActiveStatusAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'channel', 'logo_preview', 'caption', 'is_active', 'created_at']
    list_filter = ['channel', 'is_active', 'created_at']
    search_fields = ['name', 'caption', 'description', 'work_done']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['logo_preview', 'created_at', 'updated_at']
    inlines = [BrandInline]
    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'slug', 'channel', 'logo', 'logo_preview', 'caption', 'description')
        }),
        ('Client Work Story', {
            'fields': ('objective', 'stores_activated', 'team_size', 'work_done', 'achievement')
        }),
        ('Display Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="56" height="56" style="object-fit:contain;border-radius:8px;background:#fff;" />',
                obj.logo.url
            )
        return "No Logo"

    logo_preview.short_description = "Logo"


class BrandImageInline(admin.TabularInline):
    model = BrandImage
    extra = 1
    fields = ['image', 'caption', 'order']
    ordering = ['order']


class BrandProgramInline(admin.StackedInline):
    model = BrandProgram
    extra = 1
    fields = [
        'title', 'program_plan', 'customer_reach', 'objective',
        'execution_strategy', 'achievement', 'order', 'is_active'
    ]
    ordering = ['order']


@admin.register(Brand)
class BrandAdmin(ActiveStatusAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'client', 'client_channel', 'logo_preview', 'order', 'is_active', 'created_at']
    list_filter = ['client__channel', 'client', 'is_active', 'created_at']
    search_fields = ['name', 'caption', 'client__name']
    autocomplete_fields = ['client']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    readonly_fields = ['logo_preview', 'created_at']
    inlines = [BrandProgramInline, BrandImageInline]
    fieldsets = (
        ('Brand Information', {
            'fields': ('client', 'name', 'slug', 'logo', 'logo_preview', 'caption')
        }),
        ('Brand Work Story', {
            'fields': ('objective', 'outcome')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:8px;" />',
                obj.logo.url
            )
        return "No Image"

    logo_preview.short_description = "Logo Preview"

    def client_channel(self, obj):
        return obj.client.get_channel_display()

    client_channel.short_description = "Channel"


@admin.register(BrandProgram)
class BrandProgramAdmin(ActiveStatusAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'brand', 'client_name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'brand__client', 'brand', 'created_at']
    search_fields = ['title', 'brand__name', 'brand__client__name', 'program_plan', 'customer_reach']
    autocomplete_fields = ['brand']
    ordering = ['brand', 'order', 'title']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Program Information', {
            'fields': ('brand', 'title')
        }),
        ('Program Entry', {
            'fields': ('program_plan', 'customer_reach', 'objective', 'execution_strategy', 'achievement')
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def client_name(self, obj):
        return obj.brand.client.name

    client_name.short_description = "Client"


@admin.register(BrandImage)
class BrandImageAdmin(admin.ModelAdmin):
    list_display = ['brand', 'image_preview', 'order', 'caption', 'created_at']
    list_filter = ['created_at', 'brand__client', 'brand']
    search_fields = ['brand__name', 'brand__client__name', 'caption']
    autocomplete_fields = ['brand']
    ordering = ['brand', 'order']
    readonly_fields = ['image_preview', 'created_at']
    fieldsets = (
        ('Image Information', {
            'fields': ('brand', 'image', 'image_preview', 'caption', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="72" height="72" style="object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image Preview"



# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ['title', 'get_brand_display', 'featured', 'created_at']
#     list_filter = ['featured', 'brand__client', 'brand', 'created_at']
#     search_fields = ['title', 'brand__name', 'brand__client__name']
#     prepopulated_fields = {'slug': ('title',)}
#     readonly_fields = ['created_at', 'updated_at']
#     inlines = [ProjectImageInline]
#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('title', 'slug', 'brand')
#         }),
#         ('Project Details', {
#             'fields': ('objective', 'mechanisms', 'achievement')
#         }),
#         ('Display Settings', {
#             'fields': ('featured',)
#         }),
#         ('Timestamps', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def get_brand_display(self, obj):
#         """Display brand with client info in list view"""
#         return str(obj.brand)
#     get_brand_display.short_description = 'Brand'


# @admin.register(ProjectImage)
# class ProjectImageAdmin(admin.ModelAdmin):
#     list_display = ['project', 'order', 'caption', 'created_at']
#     list_filter = ['created_at', 'project']
#     search_fields = ['project__title', 'caption']
#     ordering = ['project', 'order']
#     readonly_fields = ['created_at']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'company', 'image_preview','rating', 'featured', 'created_at']
    list_filter = ['featured', 'rating', 'created_at']
    search_fields = ['client_name', 'company', 'message']
    readonly_fields = ['image_preview', 'created_at', 'updated_at']
    fieldsets = (
        ('Client Information', {
            'fields': ('client_name', 'company', 'position', 'image', 'image_preview')
        }),
        ('Testimonial', {
            'fields': ('message', 'rating')
        }),
        ('Display Settings', {
            'fields': ('featured',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:8px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image Preview"
