from django.shortcuts import render, Http404
from admin_panel.models import ProductCategory, ProductSetup, News
from .products_data import get_product_by_slug, get_all_products


class HomePageView:
    def __call__(self, request):
        news_list = News.objects.order_by('-NEWS_CREATED_AT')
        products = get_all_products()
        context = {
            'news_list': news_list,
            'products': products,
        }
        return render(request, 'core/index.html', context)


class OurProductsPageView:
    def __call__(self, request):
        selected_category = request.GET.get('category', 'all').lower()
        db_categories = ProductCategory.objects.all()
        products = get_all_products()

        if selected_category and selected_category != 'all':
            products = [
                p for p in products
                if selected_category in p['category'].lower() or selected_category in p.get('category_group', '').lower()
            ]

        context = {
            'selected_category': selected_category,
            'db_categories': db_categories,
            'products': products,
        }
        return render(request, 'pages/user/our_products.html', context)


class ProductDetailPageView:
    def __call__(self, request, slug):
        product = get_product_by_slug(slug)
        if not product:
            raise Http404(f"Product '{slug}' not found.")

        all_prods = get_all_products()
        related_products = [p for p in all_prods if p['slug'] != slug]

        context = {
            'product': product,
            'related_products': related_products,
        }
        return render(request, 'pages/user/product_detail.html', context)


class NewsDetailPageView:
    def __call__(self, request, slug):
        try:
            news_item = News.objects.get(NEWS_SLUG=slug)
        except News.DoesNotExist:
            raise Http404(f"News announcement '{slug}' not found.")

        recent_news = News.objects.exclude(id=news_item.id).order_by('-NEWS_CREATED_AT')[:4]
        context = {
            'news': news_item,
            'recent_news': recent_news,
        }
        return render(request, 'pages/user/news_detail.html', context)