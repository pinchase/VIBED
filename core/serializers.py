from rest_framework import serializers
from .models import Client, Brand, BrandProgram, BrandImage, Testimonial


class BrandImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandImage
        fields = ['id', 'image', 'caption', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class BrandProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandProgram
        fields = [
            'id', 'title', 'program_plan', 'customer_reach', 'objective',
            'execution_strategy', 'achievement', 'order', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id', 'name', 'slug', 'logo', 'caption', 'description',
            'channel', 'objective', 'stores_activated', 'team_size', 'work_done',
            'achievement', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BrandSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    programs = BrandProgramSerializer(many=True, read_only=True)
    
    class Meta:
        model = Brand
        fields = [
            'id', 'client', 'client_name', 'name', 'slug', 'logo', 'caption',
            'objective', 'outcome', 'programs', 'order',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class BrandDetailSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    images = BrandImageSerializer(many=True, read_only=True)
    programs = BrandProgramSerializer(many=True, read_only=True)
    
    class Meta:
        model = Brand
        fields = [
            'id', 'client', 'name', 'slug', 'logo', 'caption',
            'objective', 'outcome', 'programs', 'images', 'order',
            'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'id', 'client_name', 'company', 'position', 'message',
            'image', 'rating', 'featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
