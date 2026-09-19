from decimal import Decimal
from admin_panel.models import ProductSetup
from users.models import PublicUserProfile, UserCartItem


def get_authenticated_public_user(request):
    """
    Returns the logged-in PublicUserProfile instance if one exists in the session
    or through Django authentication, otherwise None.
    """
    if not hasattr(request, 'session'):
        return None
    user_id = request.session.get('public_user_id')
    if user_id:
        user = PublicUserProfile.objects.filter(id=user_id).first()
        if user:
            return user
    if hasattr(request, 'user') and request.user.is_authenticated:
        return PublicUserProfile.objects.filter(PUBLIC_USER_EMAIL__iexact=request.user.email).first()
    return None


class Cart:
    """
    Unified shopping cart manager supporting:
    1. Guest anonymous users via Django request.session['cart'].
    2. Authenticated public users via UserCartItem database models.
    3. Seamless merging of guest session cart upon user login.
    """
    SESSION_KEY = 'cart'

    def __init__(self, request):
        self.request = request
        self.session = getattr(request, 'session', {})
        self.user = get_authenticated_public_user(request)

        # Initialize session cart if not present
        if self.SESSION_KEY not in self.session:
            self.session[self.SESSION_KEY] = {}
        self.session_cart = self.session[self.SESSION_KEY]

    def _resolve_product(self, product_identifier):
        """
        Accepts integer id, numeric string id, or product slug string.
        Returns the matching ProductSetup instance or None.
        """
        if not product_identifier:
            return None
        if isinstance(product_identifier, ProductSetup):
            return product_identifier
        try:
            p_id = int(product_identifier)
            return ProductSetup.objects.filter(id=p_id).first()
        except (ValueError, TypeError):
            slug_str = str(product_identifier).strip()
            return ProductSetup.objects.filter(PRODUCT_SLUG=slug_str).first() or \
                   ProductSetup.objects.filter(PRODUCT_NAME__iexact=slug_str).first()

    def add(self, product_identifier, quantity=1, override_quantity=False):
        """
        Adds a product or increments its quantity.
        If user is logged in, saves to UserCartItem.
        If guest, saves to request.session['cart'].
        """
        product = self._resolve_product(product_identifier)
        if not product:
            return None, False

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            quantity = 1
        if quantity < 1:
            quantity = 1

        p_id_str = str(product.id)

        if self.user:
            # Save/update in database for authenticated user
            cart_item, created = UserCartItem.objects.get_or_create(
                user=self.user,
                product=product,
                defaults={'quantity': quantity}
            )
            if not created:
                if override_quantity:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity += quantity
                cart_item.save()

            # Mirror to session cart for instant local sync
            self.session_cart[p_id_str] = cart_item.quantity
            self.session.modified = True
            return product, True
        else:
            # Guest anonymous user in session
            current_qty = self.session_cart.get(p_id_str, 0)
            if override_quantity:
                new_qty = quantity
            else:
                new_qty = current_qty + quantity

            self.session_cart[p_id_str] = new_qty
            self.session.modified = True
            return product, True

    def update(self, product_identifier, quantity):
        """
        Sets explicit quantity for a product. If quantity <= 0, removes the item.
        """
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            quantity = 1

        if quantity <= 0:
            return self.remove(product_identifier)

        return self.add(product_identifier, quantity=quantity, override_quantity=True)

    def remove(self, product_identifier):
        """
        Removes a product from both user database cart and session cart.
        """
        product = self._resolve_product(product_identifier)
        if not product:
            return False

        p_id_str = str(product.id)
        removed = False

        if self.user:
            deleted_count, _ = UserCartItem.objects.filter(user=self.user, product=product).delete()
            if deleted_count > 0:
                removed = True

        if p_id_str in self.session_cart:
            del self.session_cart[p_id_str]
            self.session.modified = True
            removed = True

        return removed

    def clear(self):
        """
        Clears all items in the cart.
        """
        if self.user:
            UserCartItem.objects.filter(user=self.user).delete()
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def merge_session_cart(self, public_user):
        """
        Merges guest session cart items into the authenticated user's cart.
        Called upon successful login.
        """
        if not public_user:
            return

        session_items = dict(self.session.get(self.SESSION_KEY, {}))
        for p_id_str, qty in session_items.items():
            try:
                p_id = int(p_id_str)
                qty = int(qty)
                if qty <= 0:
                    continue
                product = ProductSetup.objects.filter(id=p_id).first()
                if not product:
                    continue

                item, created = UserCartItem.objects.get_or_create(
                    user=public_user,
                    product=product,
                    defaults={'quantity': qty}
                )
                if not created:
                    item.quantity += qty
                    item.save()
            except (ValueError, TypeError):
                continue

        # Re-sync session cart to reflect the user's complete unified cart
        merged_cart = {}
        for item in UserCartItem.objects.filter(user=public_user).select_related('product'):
            merged_cart[str(item.product.id)] = item.quantity
        self.session[self.SESSION_KEY] = merged_cart
        self.session.modified = True

    def get_items(self):
        """
        Returns structured list of items currently in the cart with full
        product metadata, quantities, and prices.
        """
        cart_map = {}  # {product_id_int: quantity}

        if self.user:
            # Query from DB for logged-in user
            db_items = UserCartItem.objects.filter(user=self.user).select_related(
                'product', 'product__PRODUCT_CATEGORY', 'product__PRODUCT_UNIT'
            )
            for item in db_items:
                cart_map[item.product_id] = item.quantity
        else:
            # Read from session for guest
            for p_id_str, qty in self.session_cart.items():
                try:
                    cart_map[int(p_id_str)] = int(qty)
                except (ValueError, TypeError):
                    continue

        if not cart_map:
            return []

        products = ProductSetup.objects.filter(id__in=cart_map.keys()).select_related(
            'PRODUCT_CATEGORY', 'PRODUCT_UNIT'
        )
        product_dict = {p.id: p for p in products}

        items = []
        for p_id, qty in cart_map.items():
            product = product_dict.get(p_id)
            if not product:
                continue

            try:
                price = float(product.PRODUCT_PRICE or 0)
            except (ValueError, TypeError):
                price = 0.0

            subtotal = price * qty

            # Format unit / packaging
            unit_str = ""
            if product.PRODUCT_UNIT:
                u_sym = product.PRODUCT_UNIT.UNIT_SYMBOL or ""
                u_name = product.PRODUCT_UNIT.UNIT_NAME or ""
                unit_str = f"{u_sym} ({u_name})" if (u_sym and u_name and u_sym != u_name) else (u_name or u_sym)
            contain = product.weight_or_size or unit_str or "Standard Pack"

            img_url = getattr(product, 'image_url', None)
            if not img_url:
                if getattr(product, 'PRODUCT_IMAGE', None):
                    try:
                        img_url = product.PRODUCT_IMAGE.url
                    except Exception:
                        img_url = f"/media/{product.PRODUCT_IMAGE}"
                else:
                    img_url = "/static/Images/fresh_herbs_extracted.png"

            cat_name = getattr(product, 'category', None)
            if not cat_name:
                if getattr(product, 'PRODUCT_CATEGORY', None):
                    cat_name = product.PRODUCT_CATEGORY.CATEGORY_NAME
                else:
                    cat_name = "Herbal Products"

            items.append({
                'id': product.id,
                'slug': getattr(product, 'slug', f"product-{product.id}"),
                'name': getattr(product, 'PRODUCT_NAME', 'Botanical Formulation'),
                'price': price,
                'price_formatted': f"Rs {int(price):,}" if price.is_integer() else f"Rs {price:,.2f}",
                'quantity': qty,
                'subtotal': subtotal,
                'subtotal_formatted': f"Rs {int(subtotal):,}" if subtotal.is_integer() else f"Rs {subtotal:,.2f}",
                'image_url': img_url,
                'contain': contain,
                'category': cat_name,
                'product': product,
            })

        return items

    def get_total_count(self):
        """
        Returns total number of items in the cart (sum of quantities).
        """
        if self.user:
            return sum(item.quantity for item in UserCartItem.objects.filter(user=self.user))
        return sum(int(qty) for qty in self.session_cart.values() if isinstance(qty, (int, str)) and str(qty).isdigit())

    def get_total_price(self):
        """
        Returns total monetary price for all items in the cart.
        """
        if self.get_total_count() == 0:
            return 0.0
        items = self.get_items()
        return sum(item['subtotal'] for item in items)
