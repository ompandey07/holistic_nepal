from django.shortcuts import render, Http404
from admin_panel.models import ProductCategory, ProductSetup
from .products_data import get_product_by_slug, get_all_products


class HomePageView:
    def __call__(self, request):
        return render(request, 'core/index.html')


class OurProductsPageView:
    def __call__(self, request):
        selected_category = request.GET.get('category', 'all').lower()
        db_categories = ProductCategory.objects.all()
        db_products = ProductSetup.objects.select_related('PRODUCT_CATEGORY', 'PRODUCT_UNIT').all()

        if selected_category and selected_category != 'all':
            db_products = db_products.filter(PRODUCT_CATEGORY__CATEGORY_NAME__icontains=selected_category)

        context = {
            'selected_category': selected_category,
            'db_categories': db_categories,
            'db_products': db_products,
        }
        return render(request, 'pages/user/our_products.html', context)


class ProductDetailPageView:
    def __call__(self, request, slug):
        product = get_product_by_slug(slug)
        if not product:
            raise Http404(f"Product '{slug}' not found.")

        all_prods = get_all_products()
        related_products = [p for p in all_prods if p['slug'] != slug][:4]

        context = {
            'product': product,
            'related_products': related_products,
        }
        return render(request, 'pages/user/product_detail.html', context)