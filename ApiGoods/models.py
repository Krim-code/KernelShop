from django.db import models
from django.template import Template, Context

class SEOProperties(models.Model):
    meta_title_template = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords_template = models.TextField(blank=True, null=True)
    meta_description_template = models.TextField(blank=True, null=True)
    element_title_template = models.CharField(max_length=255, blank=True, null=True)
    main_image_alt_template = models.CharField(max_length=255, blank=True, null=True)
    main_image_title_template = models.CharField(max_length=255, blank=True, null=True)
    main_image_filename_template = models.CharField(max_length=255, blank=True, null=True)
    detail_image_alt_template = models.CharField(max_length=255, blank=True, null=True)
    detail_image_title_template = models.CharField(max_length=255, blank=True, null=True)
    detail_image_filename_template = models.CharField(max_length=255, blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)

    def render_template(self, template_str, context):
        template = Template(template_str)
        return template.render(Context(context))

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    seo_properties = models.OneToOneField('CategorySEO', null=True, blank=True, on_delete=models.CASCADE, related_name='category_seo_properties')

    def __str__(self):
        return self.name

    def get_seo_properties(self):
        if self.seo_properties:
            return self.seo_properties
        elif self.parent:
            return self.parent.get_seo_properties()
        else:
            return None

class CategorySEO(SEOProperties):
    category = models.OneToOneField(Category, related_name='seo', on_delete=models.CASCADE)

class PropertyType(models.TextChoices):
    TEXT = 'text', 'Text'
    NUMBER = 'number', 'Number'
    DATE = 'date', 'Date'
    BOOLEAN = 'boolean', 'Boolean'

class Property(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='properties', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SingleProperty(Property):
    property_type = models.CharField(max_length=50, choices=PropertyType.choices)

class ListProperty(Property):
    pass

class ListPropertyOption(models.Model):
    list_property = models.ForeignKey(ListProperty, related_name='options', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    short_description = models.TextField()
    detailed_description = models.TextField()
    image = models.ImageField(upload_to='products/')
    sort_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    configurator = models.OneToOneField('ProductConfigurator', related_name='product', on_delete=models.CASCADE, null=True, blank=True)
    desired_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    seo_properties = models.OneToOneField('ProductSEO', null=True, blank=True, on_delete=models.CASCADE, related_name='product_seo_properties')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.final_price = self.desired_price - (self.desired_price * self.discount_percentage / 100)
        super().save(*args, **kwargs)

    def get_seo_properties(self):
        if self.seo_properties:
            return self.seo_properties
        else:
            return self.category.get_seo_properties()

class ProductSEO(SEOProperties):
    product = models.OneToOneField(Product, related_name='seo', on_delete=models.CASCADE)

class ProductSliderImage(models.Model):
    product = models.ForeignKey(Product, related_name='slider_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/slider/')

    def __str__(self):
        return f'Slider image for {self.product.name}'

class ProductFile(models.Model):
    product = models.ForeignKey(Product, related_name='files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='products/files/')
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'File for {self.product.name}'

class ProductConfigurator(models.Model):
    configuration = models.JSONField()

    def __str__(self):
        return f'Configurator for {self.id}'

class ProductProperty(models.Model):
    product = models.ForeignKey(Product, related_name='product_properties', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('product', 'property')

    def __str__(self):
        return f'{self.product.name} - {self.property.name}: {self.value}'
