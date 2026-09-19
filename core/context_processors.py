from .cart import Cart, get_authenticated_public_user


def cart_context(request):
    """
    Context processor providing cart summary data to all templates.
    """
    cart = Cart(request)
    logged_in_user = get_authenticated_public_user(request)
    total_count = cart.get_total_count()
    total_price = cart.get_total_price()

    return {
        'cart_total_count': total_count,
        'cart_total_price': total_price,
        'cart_total_price_formatted': f"Rs {int(total_price):,}" if float(total_price).is_integer() else f"Rs {total_price:,.2f}",
        'logged_in_public_user': logged_in_user,
        'is_public_user_authenticated': logged_in_user is not None,
    }
