from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Product, SingleProperty, ListPropertyOption, ProductProperty
from .forms import CategoryForm, ProductForm, CategorySEOForm, ProductSEOForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

def product_list(request, category_id=None):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id) if category_id else None
    products = Product.objects.filter(category=category) if category else Product.objects.all()
    
    # Поиск и фильтрация
    query = request.GET.get('query')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(short_description__icontains=query))

    properties = SingleProperty.objects.filter(category=category)
    for prop in properties:
        value = request.GET.get(prop.name)
        if value:
            products = products.filter(product_properties__property=prop, product_properties__value=value)

    paginator = Paginator(products, 10)  # Пагинация
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request, 'product_list.html', {
        'categories': categories,
        'category': category,
        'products': products,
        'properties': properties,
    })

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('product_list', category_id=product.category.id)
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list', category_id=product.category.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list', category_id=product.category.id)
    return render(request, 'product_confirm_delete.html', {'product': product})
