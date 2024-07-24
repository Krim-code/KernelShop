from django import forms
from django.contrib import admin
from django import forms
from .models import Product, Category, Property, SingleProperty, ListProperty, PropertyType, ProductProperty

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            properties = Property.objects.filter(category=self.instance.category)
            for property in properties:
                field_type = forms.CharField()
                if isinstance(property, SingleProperty):
                    if property.property_type == PropertyType.TEXT:
                        field_type = forms.CharField()
                    elif property.property_type == PropertyType.NUMBER:
                        field_type = forms.DecimalField()
                    elif property.property_type == PropertyType.DATE:
                        field_type = forms.DateField()
                    elif property.property_type == PropertyType.BOOLEAN:
                        field_type = forms.BooleanField()
                elif isinstance(property, ListProperty):
                    options = property.options.all()
                    choices = [(option.id, option.value) for option in options]
                    field_type = forms.ChoiceField(choices=choices)
                
                self.fields[f'property_{property.id}'] = field_type

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            for field_name, field_value in self.cleaned_data.items():
                if field_name.startswith('property_'):
                    property_id = field_name.split('_')[1]
                    property_instance = Property.objects.get(id=property_id)
                    ProductProperty.objects.update_or_create(
                        product=instance,
                        property=property_instance,
                        defaults={'value': field_value}
                    )
        return instance


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)

from django import forms
from .models import Category, Product, CategorySEO, ProductSEO, SingleProperty, ListPropertyOption, ProductProperty

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'short_description', 'detailed_description',
            'image', 'sort_order', 'is_active', 'desired_price', 'discount_percentage'
        ]

class CategorySEOForm(forms.ModelForm):
    class Meta:
        model = CategorySEO
        fields = [
            'meta_title_template', 'meta_keywords_template', 'meta_description_template',
            'element_title_template', 'main_image_alt_template', 'main_image_title_template',
            'main_image_filename_template', 'detail_image_alt_template', 'detail_image_title_template',
            'detail_image_filename_template', 'tags'
        ]

class ProductSEOForm(forms.ModelForm):
    class Meta:
        model = ProductSEO
        fields = [
            'meta_title_template', 'meta_keywords_template', 'meta_description_template',
            'element_title_template', 'main_image_alt_template', 'main_image_title_template',
            'main_image_filename_template', 'detail_image_alt_template', 'detail_image_title_template',
            'detail_image_filename_template', 'tags'
        ]
