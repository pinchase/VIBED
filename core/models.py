from django.db import models
from django.utils.text import slugify

# Write your models here.


def unique_slug_for(instance, value, *, scope=None):
    base_slug = slugify(value) or "item"
    slug = base_slug
    index = 2
    queryset = instance.__class__.objects.all()

    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.filter(slug=slug).exists():
        slug = f"{base_slug}-{index}"
        index += 1

    return slug


class Client(models.Model):
    MODERN_TRADE = 'modern_trade'
    GLOBAL_TRADE = 'global_trade'
    CHANNEL_CHOICES = [
        (MODERN_TRADE, 'Modern Trade'),
        (GLOBAL_TRADE, 'Global Trade'),
    ]

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True, max_length=200, help_text="URL slug (auto-generated if not provided)")
    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES,
        default=MODERN_TRADE,
        help_text="Select whether this client belongs to Modern Trade or Global Trade"
    )
    logo = models.ImageField(upload_to='client_logos/', blank=True, null=True, help_text="Client company logo shown on the homepage and clients page")
    caption = models.TextField(blank=True, help_text="Short line describing what the client company does")
    description = models.TextField(blank=True, null=True)
    objective = models.TextField(blank=True, help_text="The client's overall objective or brief")
    stores_activated = models.TextField(blank=True, help_text="Activation footprint, e.g. '120 stores' or 'Nairobi and Mombasa'")
    team_size = models.TextField(blank=True, help_text="Team size used for the client work")
    work_done = models.TextField(blank=True, help_text="What Braymell did for this client")
    achievement = models.TextField(blank=True, help_text="Results or achievement for this client")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name

    @property
    def is_global_trade(self):
        return self.channel == self.GLOBAL_TRADE

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided"""
        if not self.slug:
            self.slug = unique_slug_for(self, self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='brands')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=240, blank=True, help_text="URL slug (auto-generated if not provided)")
    logo = models.ImageField(upload_to='brand_logos/')
    caption = models.TextField(blank=True, help_text="Short brand summary shown on client pages")
    objective = models.TextField(blank=True, help_text="Brand objective or campaign brief")
    # execution = models.TextField(blank=True, help_text="How the brand work was executed")
    outcome = models.TextField(blank=True, help_text="Outcome or achievement from the brand work")
    order = models.PositiveIntegerField(default=0, help_text="Display priority order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        unique_together = ['client', 'name']
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return f"{self.client.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_for(self, f"{self.client.name} {self.name}")
        super().save(*args, **kwargs)


class BrandProgram(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='programs')
    title = models.CharField(max_length=200, help_text="Program name or activity title")
    program_plan = models.TextField(blank=True, help_text="Plan for this Global Trade program")
    customer_reach = models.TextField(blank=True, help_text="Customer reach for this program")
    objective = models.TextField(blank=True, help_text="Objective for this program")
    execution_strategy = models.TextField(blank=True, help_text="Execution strategy for this program")
    achievement = models.TextField(blank=True, help_text="Achievement or result for this program")
    order = models.PositiveIntegerField(default=0, help_text="Display priority order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Brand Program"
        verbose_name_plural = "Brand Programs"

    def __str__(self):
        return f"{self.brand.name} - {self.title}"


class BrandImage(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='brand_images/')
    caption = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order in gallery")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Brand Image"
        verbose_name_plural = "Brand Images"

    def __str__(self):
        return f"{self.brand.name} - Image {self.order}"


class Project(models.Model):
    title = models.CharField(
        max_length=200,
        help_text="Project title (e.g., 'Dettol Campaign')"
    )
    slug = models.SlugField(
        unique=True,
        max_length=200,
        help_text="URL slug (auto-generated if not provided)"
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name='projects',
        help_text="Brand this project is associated with"
    )
    objective = models.TextField(
        help_text="Project objective and goals"
    )
    mechanisms = models.TextField(
        help_text="How the project was executed"
    )
    achievement = models.TextField(
        help_text="Results and achievements"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Display on homepage"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug from title if not provided"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectImage(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='project_images/')
    caption = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order in gallery"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"

    def __str__(self):
        return f"{self.project.title} - Image {self.order}"


class Testimonial(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    client_name = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField()
    image = models.ImageField(upload_to='testimonial_images/', null=True, blank=True)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        default=5
    )
    featured = models.BooleanField(default=False, help_text="Display on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.client_name} - {self.company}"
