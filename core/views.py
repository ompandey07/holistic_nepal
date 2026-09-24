import json
from django.shortcuts import render, redirect, Http404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import DetailView, TemplateView
from admin_panel.models import ProductCategory, ProductSetup, ProductRating, ProductOrder, News, HospitalInfo, HospitalService, HospitalServiceTag, Service, Gallery, GalleryImage
from users.models import PublicUserProfile
from .products_data import get_product_by_slug, get_all_products
from .cart import Cart, get_authenticated_public_user


class HomePageView:
    def __call__(self, request):
        news_list = News.objects.prefetch_related('NEWS_IMAGES').order_by('-NEWS_CREATED_AT')
        products = ProductSetup.objects.select_related('PRODUCT_CATEGORY', 'PRODUCT_UNIT').prefetch_related('PRODUCT_RATINGS', 'PRODUCT_RATINGS__PRODUCT_RATING_USER').order_by('-PRODUCT_CREATED_AT')
        categories = ProductCategory.objects.all().order_by('id')
        context = {
            'news_list': news_list,
            'products': products,
            'categories': categories,
        }
        return render(request, 'core/index.html', context)


from django.utils.text import slugify


class OurProductsPageView:
    def __call__(self, request):
        selected_category = request.GET.get('category', 'all').strip().lower()
        db_categories = list(ProductCategory.objects.all().order_by('id'))
        all_products = list(
            ProductSetup.objects.select_related('PRODUCT_CATEGORY', 'PRODUCT_UNIT')
            .order_by('-PRODUCT_CREATED_AT')
        )

        categories_data = []
        for cat in db_categories:
            c_slug = cat.slug
            cat_prods = [p for p in all_products if p.PRODUCT_CATEGORY_id == cat.id]
            is_active = (selected_category != 'all' and (selected_category == c_slug or selected_category == str(cat.id)))

            # Aesthetic icon assignment
            c_lower = cat.CATEGORY_NAME.lower()
            if any(k in c_lower for k in ['tea', 'beverage', 'drink', 'coffee']):
                icon_type = 'tea'
            elif any(k in c_lower for k in ['care', 'oil', 'skin', 'oral', 'dental', 'soap', 'body', 'personal']):
                icon_type = 'droplet'
            else:
                icon_type = 'leaf'

            categories_data.append({
                'id': cat.id,
                'name': cat.CATEGORY_NAME,
                'slug': c_slug,
                'tag': getattr(cat, 'CATEGORY_TAG', None) or cat.CATEGORY_NAME,
                'desc': f"Pure Himalayan formulations under {cat.CATEGORY_NAME}.",
                'icon_type': icon_type,
                'products': cat_prods,
                'count': len(cat_prods),
                'is_active': is_active,
            })

        # Filtered categories if a specific filter is selected in query string
        if selected_category and selected_category != 'all':
            visible_categories = [c for c in categories_data if c['is_active']]
            if not visible_categories:
                visible_categories = categories_data
        else:
            visible_categories = categories_data

        context = {
            'selected_category': selected_category,
            'db_categories': db_categories,
            'categories_data': categories_data,
            'visible_categories': visible_categories,
            'all_products': all_products,
            'total_products_count': len(all_products),
        }
        return render(request, 'pages/user/our_products.html', context)


class ProductDetailPageView:
    def get_logged_in_user(self, request):
        user_id = request.session.get('public_user_id') if hasattr(request, 'session') else None
        if user_id:
            try:
                return PublicUserProfile.objects.get(id=user_id)
            except PublicUserProfile.DoesNotExist:
                pass
        if hasattr(request, 'user') and request.user.is_authenticated and getattr(request.user, 'email', None):
            return PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL=request.user.email).first()
        return None

    def __call__(self, request, slug):
        product = get_product_by_slug(slug)
        if not product:
            raise Http404(f"Product '{slug}' not found.")

        # Underlying database instance for relations
        db_product = ProductSetup.objects.filter(PRODUCT_SLUG=slug).first()
        if not db_product and product.get('db_id'):
            db_product = ProductSetup.objects.filter(id=product['db_id']).first()

        logged_in_user = self.get_logged_in_user(request)

        # Handle POST review submission
        if request.method == 'POST':
            if not logged_in_user:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': 'You must be logged in to rate this product.'}, status=403)
                login_url = reverse('login')
                return redirect(f"{login_url}?next={request.path}")

            if not db_product:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': 'Product record not found in database.'}, status=404)
                return redirect(request.path)

            rating_raw = request.POST.get('rating', '5')
            comment_text = request.POST.get('comment', '').strip()

            try:
                rating_val = float(rating_raw)
                if not (1.0 <= rating_val <= 5.0):
                    rating_val = 5.0
            except (ValueError, TypeError):
                rating_val = 5.0

            # One review per user per product: update existing or create new
            existing_review = ProductRating.objects.filter(
                PRODUCT_RATING_PRODUCT=db_product,
                PRODUCT_RATING_USER=logged_in_user
            ).first()

            if existing_review:
                existing_review.PRODUCT_RATING_VALUE = rating_val
                existing_review.COMMENT_ENG = comment_text
                existing_review.PRODUCT_RATING_COMMENT = comment_text
                existing_review.IS_VERIFIED = True
                existing_review.save()
                msg = "Your botanical review has been updated successfully!"
            else:
                ProductRating.objects.create(
                    PRODUCT_RATING_PRODUCT=db_product,
                    PRODUCT_RATING_USER=logged_in_user,
                    PRODUCT_RATING_VALUE=rating_val,
                    COMMENT_ENG=comment_text,
                    PRODUCT_RATING_COMMENT=comment_text,
                    IS_VERIFIED=True,
                    IS_FEATURED=False
                )
                msg = "Thank you! Your botanical review has been submitted successfully."

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': msg})

            try:
                messages.success(request, msg)
            except Exception:
                pass
            return redirect(f"{request.path}#reviews")

        # GET request context
        product_reviews = []
        user_review = None
        if db_product:
            import html
            import re
            from django.utils.html import strip_tags

            product['name'] = db_product.PRODUCT_NAME
            product['price_display'] = db_product.price_display
            product['price_formatted'] = db_product.price_formatted
            product['category'] = db_product.category
            product['category_group'] = db_product.category
            product['short_desc'] = db_product.short_desc
            product['english_desc'] = db_product.short_desc
            product['nepali_desc'] = db_product.short_desc
            product['image_url'] = db_product.image_url

            # Unit / Contain strictly from DB
            unit_str = ""
            if db_product.PRODUCT_UNIT:
                u_sym = db_product.PRODUCT_UNIT.UNIT_SYMBOL or ""
                u_name = db_product.PRODUCT_UNIT.UNIT_NAME or ""
                unit_str = f"{u_sym} ({u_name})" if (u_sym and u_name and u_sym != u_name) else (u_name or u_sym)
            product['contain'] = db_product.weight_or_size or unit_str or "Standard Pack"

            # Gallery images
            gallery_images = [db_product.image_url]
            for p_img in db_product.PRODUCT_IMAGES.all():
                try:
                    gallery_images.append(p_img.IMAGE.url)
                except Exception:
                    gallery_images.append(f"/media/{p_img.IMAGE}")
            product['gallery_images'] = gallery_images

            # Rating strictly from DB
            if db_product.avg_rating:
                product['rating'] = db_product.avg_rating
                product['reviews_count'] = db_product.reviews_count
                product['avg_rating_stars'] = db_product.avg_rating_stars
            else:
                product['rating'] = None
                product['reviews_count'] = 0
                product['avg_rating_stars'] = ""

            # Extract clean highlights from PRODUCT_KEY_FEATURES or short_desc
            feat_source = db_product.PRODUCT_KEY_FEATURES or db_product.PRODUCT_DESCRIPTION or ""
            if feat_source:
                formatted_feat = re.sub(r'</?(?:p|li|div|br\s*/?|h[1-6])[^>]*>', '\n', feat_source, flags=re.IGNORECASE)
                clean_feat = html.unescape(strip_tags(formatted_feat)).replace('\xa0', ' ')
                lines = [l.strip(' -*•\r\t') for l in clean_feat.split('\n') if l.strip(' -*•\r\t')]
            else:
                lines = []
            product['highlights'] = lines[:5] if lines else [
                "100% Pure authentic Himalayan herbal formulation",
                "Processed under strict traditional Ayurvedic standards",
                "Lab verified for chemical purity and active botanicals",
                "Zero artificial additives, preservatives or harsh chemicals"
            ]

            # Direct real reviews strictly for this specific product only
            product_reviews = list(
                db_product.PRODUCT_RATINGS.select_related('PRODUCT_RATING_USER')
                .order_by('-PRODUCT_RATING_CREATED_AT')
            )

            if logged_in_user:
                user_review = db_product.PRODUCT_RATINGS.filter(PRODUCT_RATING_USER=logged_in_user).first()

            # Real companion products strictly from database
            related_products = list(
                ProductSetup.objects.exclude(id=db_product.id)
                .select_related('PRODUCT_CATEGORY', 'PRODUCT_UNIT')
                .order_by('-PRODUCT_CREATED_AT')[:8]
            )
        else:
            all_prods = get_all_products()
            related_products = [p for p in all_prods if p['slug'] != slug]

        context = {
            'product': product,
            'db_product': db_product,
            'related_products': related_products,
            'logged_in_user': logged_in_user,
            'product_reviews': product_reviews,
            'user_review': user_review,
        }
        return render(request, 'pages/user/product_detail.html', context)


class NewsListPageView:
    def __call__(self, request):
        category_filter = request.GET.get('category', 'all').strip().upper()
        news_qs = News.objects.prefetch_related('NEWS_IMAGES').order_by('-NEWS_CREATED_AT')

        if category_filter and category_filter != 'ALL':
            news_qs = news_qs.filter(NEWS_TYPE=category_filter)

        news_types = [choice[0] for choice in News._meta.get_field('NEWS_TYPE').choices]

        context = {
            'news_list': news_qs,
            'news_types': news_types,
            'selected_category': category_filter,
            'total_count': news_qs.count(),
        }
        return render(request, 'pages/user/news_list.html', context)


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


class HospitalPageView:
    def __call__(self, request):
        hospital_info = HospitalInfo.objects.filter(IS_ACTIVE=True).first()
        services = Service.objects.all().order_by('order', 'id')
        legacy_services = list(HospitalService.objects.filter(IS_ACTIVE=True).order_by('SERVICE_ORDER', 'id'))
        service_tags = list(HospitalServiceTag.objects.filter(IS_ACTIVE=True).order_by('TAG_ORDER', 'id'))

        cart_total_count = 0
        try:
            cart = Cart(request)
            cart_total_count = cart.get_total_count()
        except Exception:
            pass

        context = {
            'hospital_info': hospital_info,
            'services': services,
            'legacy_services': legacy_services,
            'service_tags': service_tags,
            'cart_total_count': cart_total_count,
        }
        return render(request, 'pages/user/hospital.html', context)


class HospitalServiceDetailView(DetailView):
    model = Service
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'pages/user/service_detail.html'
    context_object_name = 'service'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hospital_info'] = HospitalInfo.objects.filter(IS_ACTIVE=True).first()
        cart_total_count = 0
        try:
            cart = Cart(self.request)
            cart_total_count = cart.get_total_count()
        except Exception:
            pass
        context['cart_total_count'] = cart_total_count
        return context


class GalleryPageView(TemplateView):
    """
    Public-facing Botanical Gallery Showcase page view.
    Renders album cards grid and interactive lightbox with sample gallery datasets.
    """
    template_name = 'pages/user/gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hospital_info = HospitalInfo.objects.filter(IS_ACTIVE=True).first()
        cart_total_count = 0
        try:
            cart = Cart(self.request)
            cart_total_count = cart.get_total_count()
        except Exception:
            pass

        # Query real database gallery albums created via the admin panel
        gallery_qs = (
            Gallery.objects
            .prefetch_related('GALLERY_IMAGES')
            .order_by('-GALLERY_CREATED_AT')
        )

        albums = []
        for item in gallery_qs:
            photos = []
            for img in item.GALLERY_IMAGES.all():
                if img.IMAGE:
                    photos.append({
                        'url': img.IMAGE.url,
                        'caption_en': item.GALLERY_TITLE,
                        'caption_np': item.GALLERY_TITLE,
                    })

            cover_url = ''
            if item.GALLERY_IMAGE:
                cover_url = item.GALLERY_IMAGE.url
            elif photos:
                cover_url = photos[0]['url']

            albums.append({
                'id': item.id,
                'slug': item.GALLERY_SLUG or f"album-{item.id}",
                'title_en': item.GALLERY_TITLE,
                'title_np': item.GALLERY_TITLE,
                'caption_en': item.GALLERY_DESCRIPTION,
                'caption_np': item.GALLERY_DESCRIPTION,
                'cover_image': cover_url,
                'image_count': len(photos),
                'photos': photos,
            })

        context['hospital_info'] = hospital_info
        context['cart_total_count'] = cart_total_count
        context['albums'] = albums
        context['total_albums'] = len(albums)
        context['total_photos'] = sum(album['image_count'] for album in albums)
        return context



# ==============================================================================
# SHOPPING BASKET / CART & CHECKOUT VIEWS
# ==============================================================================

class CartPageView:
    """
    Renders the botanical cart/basket page.
    ACCESSIBILITY: Open to ALL users (guests and authenticated accounts).
    """
    def __call__(self, request):
        cart = Cart(request)
        cart_items = cart.get_items()
        total_items = cart.get_total_count()
        subtotal = cart.get_total_price()

        # Transparent Ayurvedic Delivery calculation: Free shipping over Rs 2,500
        free_shipping_threshold = 2500.0
        shipping_fee = 0.0 if (subtotal >= free_shipping_threshold or subtotal == 0) else 120.0
        grand_total = subtotal + shipping_fee

        user = get_authenticated_public_user(request)

        context = {
            'cart_items': cart_items,
            'total_items': total_items,
            'subtotal': subtotal,
            'subtotal_formatted': f"Rs {int(subtotal):,}" if float(subtotal).is_integer() else f"Rs {subtotal:,.2f}",
            'shipping_fee': shipping_fee,
            'shipping_fee_formatted': "FREE" if shipping_fee == 0 else f"Rs {int(shipping_fee):,}",
            'grand_total': grand_total,
            'grand_total_formatted': f"Rs {int(grand_total):,}" if float(grand_total).is_integer() else f"Rs {grand_total:,.2f}",
            'is_logged_in': user is not None,
            'user': user,
            'free_shipping_threshold': free_shipping_threshold,
            'amount_for_free_shipping': max(0.0, free_shipping_threshold - subtotal),
        }
        return render(request, 'pages/user/cart.html', context)


class AddToCartAPIView:
    """
    AJAX endpoint to add an item to the shopping cart.
    ACCESSIBILITY: Open to ALL users (guests and authenticated accounts).
    Does NOT require login, does NOT redirect.
    """
    def __call__(self, request):
        if request.method != 'POST':
            return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

        product_id = request.POST.get('product_id') or request.POST.get('slug')
        quantity = request.POST.get('quantity', 1)

        if not product_id and request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
                if isinstance(data, dict):
                    product_id = data.get('product_id') or data.get('slug')
                    quantity = data.get('quantity', 1)
            except Exception:
                pass

        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'Product identifier missing.'}, status=400)

        cart = Cart(request)
        product, added = cart.add(product_id, quantity=quantity)

        if not product:
            return JsonResponse({'status': 'error', 'message': 'Botanical product not found.'}, status=404)

        return JsonResponse({
            'status': 'success',
            'message': f"'{product.PRODUCT_NAME}' added to your botanical basket.",
            'product_id': product.id,
            'product_name': product.PRODUCT_NAME,
            'cart_count': cart.get_total_count(),
            'cart_total': cart.get_total_price(),
        })


class UpdateCartAPIView:
    """
    AJAX endpoint to update item quantities in the cart.
    """
    def __call__(self, request):
        if request.method != 'POST':
            return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)

        if not product_id and request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
                if isinstance(data, dict):
                    product_id = data.get('product_id')
                    quantity = data.get('quantity', 1)
            except Exception:
                pass

        cart = Cart(request)
        cart.update(product_id, quantity)

        # Retrieve updated line item subtotal
        items = cart.get_items()
        item_subtotal = 0.0
        for it in items:
            if str(it['id']) == str(product_id) or str(it['slug']) == str(product_id):
                item_subtotal = it['subtotal']
                break

        subtotal = cart.get_total_price()
        free_shipping_threshold = 2500.0
        shipping_fee = 0.0 if (subtotal >= free_shipping_threshold or subtotal == 0) else 120.0
        grand_total = subtotal + shipping_fee

        return JsonResponse({
            'status': 'success',
            'cart_count': cart.get_total_count(),
            'cart_total': subtotal,
            'cart_total_formatted': f"Rs {int(subtotal):,}" if float(subtotal).is_integer() else f"Rs {subtotal:,.2f}",
            'item_subtotal_formatted': f"Rs {int(item_subtotal):,}" if float(item_subtotal).is_integer() else f"Rs {item_subtotal:,.2f}",
            'shipping_fee_formatted': "FREE" if shipping_fee == 0 else f"Rs {int(shipping_fee):,}",
            'grand_total_formatted': f"Rs {int(grand_total):,}" if float(grand_total).is_integer() else f"Rs {grand_total:,.2f}",
            'amount_for_free_shipping': max(0.0, free_shipping_threshold - subtotal),
        })


class RemoveFromCartAPIView:
    """
    AJAX endpoint to remove an item from the cart entirely.
    """
    def __call__(self, request):
        if request.method != 'POST':
            return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

        product_id = request.POST.get('product_id')
        if not product_id and request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
                if isinstance(data, dict):
                    product_id = data.get('product_id')
            except Exception:
                pass

        cart = Cart(request)
        cart.remove(product_id)

        subtotal = cart.get_total_price()
        free_shipping_threshold = 2500.0
        shipping_fee = 0.0 if (subtotal >= free_shipping_threshold or subtotal == 0) else 120.0
        grand_total = subtotal + shipping_fee

        return JsonResponse({
            'status': 'success',
            'cart_count': cart.get_total_count(),
            'cart_total': subtotal,
            'cart_total_formatted': f"Rs {int(subtotal):,}" if float(subtotal).is_integer() else f"Rs {subtotal:,.2f}",
            'shipping_fee_formatted': "FREE" if shipping_fee == 0 else f"Rs {int(shipping_fee):,}",
            'grand_total_formatted': f"Rs {int(grand_total):,}" if float(grand_total).is_integer() else f"Rs {grand_total:,.2f}",
            'amount_for_free_shipping': max(0.0, free_shipping_threshold - subtotal),
        })


class CartCountAPIView:
    """
    AJAX endpoint to fetch the current total count and price for the cart.
    """
    def __call__(self, request):
        cart = Cart(request)
        return JsonResponse({
            'cart_count': cart.get_total_count(),
            'cart_total': cart.get_total_price(),
        })


class CheckoutPageView:
    """
    Checkout page view.
    STRICT SECURITY GATE: REQUIRES AUTHENTICATED PUBLIC USER PROFILE.
    If unauthenticated, permanently redirects to /login/?next=/checkout/.
    """
    def __call__(self, request):
        user = get_authenticated_public_user(request)
        if not user:
            checkout_url = reverse('checkout')
            login_url = f"{reverse('login')}?next={checkout_url}"
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'login_required', 'redirect_url': login_url}, status=401)
            return redirect(login_url)

        cart = Cart(request)
        cart_items = cart.get_items()
        subtotal = cart.get_total_price()

        free_shipping_threshold = 2500.0
        shipping_fee = 0.0 if (subtotal >= free_shipping_threshold or subtotal == 0) else 120.0
        grand_total = subtotal + shipping_fee

        # --- HANDLE REAL ORDER PLACEMENT (POST) ---
        if request.method == 'POST':
            if not cart_items:
                return JsonResponse({'status': 'error', 'message': 'Your basket is empty. Please select botanical formulations to purchase.'}, status=400)

            data = {}
            if request.content_type == 'application/json' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
                try:
                    if request.body:
                        data = json.loads(request.body.decode('utf-8'))
                except Exception:
                    data = {}
            if not data:
                data = request.POST

            full_name = data.get('full_name') if 'full_name' in data else user.PUBLIC_USER_FULL_NAME
            full_name = (full_name or '').strip()
            email = data.get('email') if 'email' in data else user.PUBLIC_USER_EMAIL
            email = (email or '').strip()
            mobile_no = data.get('mobile_no') if 'mobile_no' in data else user.PUBLIC_USER_MOBILE_NO
            mobile_no = (mobile_no or '').strip()
            address = data.get('address') if 'address' in data else user.PUBLIC_USER_ADDRESS
            address = (address or '').strip()
            delivery_instructions = (data.get('delivery_instructions') or '').strip()
            payment_method = (data.get('payment_method') or 'COD').strip().upper()

            if not full_name:
                return JsonResponse({'status': 'error', 'message': 'Full name is required for order fulfillment.'}, status=400)
            if not mobile_no:
                return JsonResponse({'status': 'error', 'message': 'Contact phone number is required for dispatch courier.'}, status=400)
            if not address:
                return JsonResponse({'status': 'error', 'message': 'Detailed delivery address is required for dispatch.'}, status=400)

            # Build items snapshot and compute total item quantity
            items_snapshot = []
            primary_product = None
            total_qty = 0
            for it in cart_items:
                p_id = it.get('id') or it.get('db_id')
                qty = int(it.get('quantity', 1))
                price = float(it.get('price', 0))
                item_subtotal = float(it.get('subtotal', price * qty))
                items_snapshot.append({
                    'id': p_id,
                    'name': it.get('name', ''),
                    'slug': it.get('slug', ''),
                    'price': price,
                    'quantity': qty,
                    'subtotal': item_subtotal,
                    'image_url': it.get('image_url', ''),
                    'contain': it.get('contain', ''),
                })
                total_qty += qty
                if not primary_product and p_id:
                    primary_product = ProductSetup.objects.filter(id=p_id).first()

            try:
                order = ProductOrder.objects.create(
                    CUSTOMER=user,
                    PRODUCT_ORDER_PRODUCT=primary_product,
                    PRODUCT_ORDER_QTY=total_qty or 1,
                    PRODUCT_ORDER_STATUS="PENDING",
                    TOTAL_AMOUNT=grand_total,
                    SHIPPING_FEE=shipping_fee,
                    SHIPPING_NAME=full_name,
                    SHIPPING_EMAIL=email,
                    SHIPPING_PHONE=mobile_no,
                    SHIPPING_ADDRESS=address,
                    DELIVERY_INSTRUCTIONS=delivery_instructions,
                    PAYMENT_METHOD=payment_method,
                    ORDER_ITEMS_DATA=items_snapshot,
                    ORDER_SOURCE="WEB",
                    IS_PAID=(payment_method in ["ESEWA", "KHALTI"]),
                )
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Order creation failed: {str(e)}'}, status=500)

            # Clear cart on success
            cart.clear()

            return JsonResponse({
                'status': 'success',
                'message': f'Order #{order.PRODUCT_ORDER_ID} placed successfully!',
                'order_id': order.PRODUCT_ORDER_ID,
                'order_db_id': order.id,
                'order_date': order.PRODUCT_ORDER_CREATED_AT.strftime('%Y-%m-%d'),
                'total_amount': float(grand_total),
                'total_amount_formatted': f"Rs {int(grand_total):,}" if float(grand_total).is_integer() else f"Rs {grand_total:,.2f}",
                'client_name': full_name,
                'delivery_address': address,
                'payment_method': payment_method,
                'items_count': total_qty,
                'redirect_url': reverse('user_orders'),
            })

        # --- RENDER CHECKOUT PAGE (GET) ---
        if not cart_items:
            messages.info(request, "Your basket is currently empty. Please select remedies to purchase.")
            return redirect('cart')

        context = {
            'user': user,
            'cart_items': cart_items,
            'total_items': cart.get_total_count(),
            'subtotal': subtotal,
            'subtotal_formatted': f"Rs {int(subtotal):,}" if float(subtotal).is_integer() else f"Rs {subtotal:,.2f}",
            'shipping_fee': shipping_fee,
            'shipping_fee_formatted': "FREE" if shipping_fee == 0 else f"Rs {int(shipping_fee):,}",
            'grand_total': grand_total,
            'grand_total_formatted': f"Rs {int(grand_total):,}" if float(grand_total).is_integer() else f"Rs {grand_total:,.2f}",
        }
        return render(request, 'pages/user/checkout.html', context)


# ==============================================================================
# -- DEDICATED PUBLIC ORDER TRACKING VIEW --------------------------------------
# ==============================================================================
class TrackOrderPageView(TemplateView):
    """
    Public order tracking page.
    Allows guests and authenticated users to track the status of an order using
    the Order Number (#ORD-000005, ORD-000005, 000005) plus phone or email verification.
    """
    template_name = 'pages/user/track_order.html'

    def get(self, request, *args, **kwargs):
        order_id = request.GET.get('order_id', '').strip()
        return self._handle_lookup(request, order_id, is_post=False)

    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id', '').strip()
        return self._handle_lookup(request, order_id, is_post=True)

    def _handle_lookup(self, request, raw_order_id, is_post):
        import re
        searched = bool(raw_order_id or is_post)
        order = None
        error_message = None
        items_list = []
        status_step = 1
        is_cancelled = False

        if searched:
            if not raw_order_id:
                error_message = "Please enter your order number."
            else:
                order = self._find_order(raw_order_id)
                if not order:
                    error_message = "Order not found — check your order number."
                else:
                    items_list = self._get_items_list(order)
                    st = (order.PRODUCT_ORDER_STATUS or "PENDING").upper()
                    if st == "CANCELLED":
                        is_cancelled = True
                        status_step = 0
                    elif st == "CONFIRMED":
                        status_step = 2
                    elif st == "PROCESSING":
                        status_step = 3
                    elif st in ["SHIPPED", "DISPATCHED"]:
                        status_step = 4
                    elif st == "DELIVERED":
                        status_step = 5
                    else: # PENDING or default
                        status_step = 1

        context = {
            'searched': searched,
            'order_id_query': raw_order_id,
            'order': order,
            'items_list': items_list,
            'error_message': error_message,
            'status_step': status_step,
            'is_cancelled': is_cancelled,
        }
        return render(request, self.template_name, context)

    def _find_order(self, raw_order_id):
        import re
        cleaned = raw_order_id.strip().upper().lstrip('#').strip()
        candidates = [cleaned]

        digits = re.findall(r'\d+', cleaned)
        if digits:
            num_val = int(digits[-1])
            candidates.append(f"ORD-{num_val:06d}")
            candidates.append(f"ORD-{num_val}")
            candidates.append(f"{num_val:06d}")
            candidates.append(str(num_val))

        order = None
        for cand in candidates:
            order = ProductOrder.objects.filter(PRODUCT_ORDER_ID__iexact=cand).first()
            if order:
                break

        if not order and digits and digits[-1].isdigit():
            order = ProductOrder.objects.filter(id=int(digits[-1])).first()

        return order

    def _get_items_list(self, order):
        items = []
        if order.ORDER_ITEMS_DATA and isinstance(order.ORDER_ITEMS_DATA, list):
            for it in order.ORDER_ITEMS_DATA:
                try:
                    price = float(it.get('price', 0))
                except Exception:
                    price = 0.0
                try:
                    qty = int(it.get('quantity', 1))
                except Exception:
                    qty = 1
                try:
                    subtotal = float(it.get('subtotal', price * qty))
                except Exception:
                    subtotal = price * qty
                items.append({
                    'name': it.get('name', 'Ayurvedic Formulation'),
                    'slug': it.get('slug', ''),
                    'quantity': qty,
                    'price': price,
                    'price_formatted': f"Rs {int(price):,}" if price.is_integer() else f"Rs {price:,.2f}",
                    'subtotal': subtotal,
                    'subtotal_formatted': f"Rs {int(subtotal):,}" if subtotal.is_integer() else f"Rs {subtotal:,.2f}",
                    'image_url': it.get('image_url', ''),
                    'contain': it.get('contain', ''),
                })
        elif order.PRODUCT_ORDER_PRODUCT:
            p = order.PRODUCT_ORDER_PRODUCT
            qty = int(order.PRODUCT_ORDER_QTY) if order.PRODUCT_ORDER_QTY else 1
            price = float(p.PRODUCT_PRICE) if p.PRODUCT_PRICE else 0.0
            subtotal = price * qty
            img_url = p.PRODUCT_IMAGE.url if p.PRODUCT_IMAGE else ''
            items.append({
                'name': p.PRODUCT_NAME,
                'slug': getattr(p, 'slug', ''),
                'quantity': qty,
                'price': price,
                'price_formatted': f"Rs {int(price):,}" if price.is_integer() else f"Rs {price:,.2f}",
                'subtotal': subtotal,
                'subtotal_formatted': f"Rs {int(subtotal):,}" if subtotal.is_integer() else f"Rs {subtotal:,.2f}",
                'image_url': img_url,
                'contain': f"{p.PRODUCT_CONTAIN} {p.PRODUCT_UNIT}" if p.PRODUCT_CONTAIN else '',
            })
        return items


# ==============================================================================
# -- CUSTOM ERROR HANDLERS (404 & 500) -----------------------------------------
# ==============================================================================
def custom_404_view(request, exception=None):
    """Custom 404 error view rendering branded 404 template with HTTP 404 status."""
    return render(request, '404.html', status=404)


def custom_500_view(request):
    """Custom 500 error view rendering branded 500 template with HTTP 500 status."""
    return render(request, '500.html', status=500)

