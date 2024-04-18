from django.shortcuts import get_object_or_404
from classes.models import Lesson


# The cart_contents function will be used in all views that require the cart to be displayed.
def cart_contents(request):
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for item_id, quantity in cart.items():
        lesson = get_object_or_404(Lesson, pk=item_id)
        total += quantity * lesson.cost
        cart_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'lesson': lesson,
        })
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
    }

    return context
