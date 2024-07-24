from django.contrib import admin
from .models import Category, SingleProperty, ListProperty, ListPropertyOption, Product, ProductProperty, ProductConfigurator, ProductSliderImage, ProductFile, CategorySEO, ProductSEO
from django.contrib.admin import StackedInline

class CategorySEOInline(StackedInline):
    model = CategorySEO
    extra = 0

class ProductSEOInline(StackedInline):
    model = ProductSEO
    extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    inlines = [CategorySEOInline]

class SinglePropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'property_type')
    list_filter = ('category', 'property_type')
    search_fields = ('name',)

class ListPropertyOptionInline(admin.TabularInline):
    model = ListPropertyOption
    extra = 1

class ListPropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
    inlines = [ListPropertyOptionInline]

class ProductPropertyInline(admin.TabularInline):
    model = ProductProperty
    extra = 1

class ProductSliderImageInline(admin.TabularInline):
    model = ProductSliderImage
    extra = 1

class ProductFileInline(admin.TabularInline):
    model = ProductFile
    extra = 1

class ProductConfiguratorAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'sort_order', 'desired_price', 'discount_percentage', 'final_price')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'short_description', 'detailed_description')
    inlines = [ProductPropertyInline, ProductSliderImageInline, ProductFileInline, ProductSEOInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(SingleProperty, SinglePropertyAdmin)
admin.site.register(ListProperty, ListPropertyAdmin)
admin.site.register(ProductConfigurator, ProductConfiguratorAdmin)
admin.site.register(Product, ProductAdmin)
