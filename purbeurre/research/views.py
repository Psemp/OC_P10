from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
import logging

from .script.compare import get_product_categories, get_similar_prod
from .script.compare import compare_products
from .models import Product

# Logger

logger = logging.getLogger(__name__)

# Create your views here.


def index(request):
    return render(request, 'research/index.html')


def compare(request, product_id):
    user_product = get_object_or_404(Product, pk=product_id)
    cat_set = get_product_categories(user_product)
    similar_products = get_similar_prod(cat_set)
    prod_list = compare_products(user_product, similar_products)
    title = f"Produits plus sain que {user_product.name}"

    paginator = Paginator(prod_list, 9)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        "products": products,
        "title": title
    }

    logger.info('New comparison', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })

    return render(request, 'research/compare.html', context)


def search(request):
    query = request.GET.get('query')
    if not query:
        prod_list = -1
    else:
        prod_list = Product.objects.filter(name__icontains=query)
    if not prod_list.exists():
        prod_list = Product.objects.filter(brand__icontains=query)

    title = f"Produits correspondants à {query}"
    user_query = f"?query={query}"

    paginator = Paginator(prod_list, 9)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'title': title,
        'user_query': user_query
    }

    logger.info('New research', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })

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
