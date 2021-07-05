from django.shortcuts import render, get_object_or_404
from .script.compare import get_product_categories, get_similar_prod
from .script.compare import compare_products
from .models import Product

# Create your views here.


def index(request):
    return render(request, 'research/index.html')


def compare(request, product_id):
    user_product = get_object_or_404(Product, pk=product_id)
    cat_set = get_product_categories(user_product)
    similar_products = get_similar_prod(cat_set)
    products = compare_products(user_product, similar_products)
    title = f"Produits plus sain que {user_product.name}"
    context = {
        "products": products,
        "title": title
    }

    return render(request, 'research/compare.html', context)


def search(request):
    query = request.GET.get('query')
    if not query:
        products = -1
    else:
        products = Product.objects.filter(name__icontains=query)
    if not products.exists():
        products = Product.objects.filter(brand__icontains=query)

    title = f"Produits correspondants à {query}"

    context = {
        'products': products,
        'title': title
    }

    return render(request, 'research/search.html', context)


def legal(request):
    return render(request, 'research/mentions_legales.html')


def error_404(request, exception):
    context = {}
    return render(request, 'research/404.html', context)


def error_500(request):
    context = {}
    return render(request, 'research/500.html', context)


def error_403(request, exception):
    context = {}
    return render(request, 'research/403.html', context)


def error_400(request, exception):
    context = {}
    return render(request, 'research/400.html', context)
