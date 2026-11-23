from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from cart.forms import CartAddProductForm
from .models import Category, Product


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).select_related('category').prefetch_related('images')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # 1. Пошук за назвою або описом
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # 2. Фільтри (діапазон цін та наявність)
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    in_stock = request.GET.get('in_stock')

    if min_price.isdigit():
        products = products.filter(price__gte=min_price)
    if max_price.isdigit():
        products = products.filter(price__lte=max_price)
    if in_stock == '1':
        products = products.filter(stock__gt=0)

    # 3. Сортування
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-id')

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'in_stock': in_stock,
        'sort': sort,
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images'),
        id=id,
        slug=slug,
        available=True
    )
    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'shop/product/detail.html', context)