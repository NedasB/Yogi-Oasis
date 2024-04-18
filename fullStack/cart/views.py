from django.shortcuts import render, redirect


def view_cart(request):
    """A view that renders the cart contents page."""
    cart = request.session.get('cart', {})
    return render(request, "cart/cart.html", {'cart': cart})


def add_to_cart(request, class_id):
    """Add lesson spaces to the cart."""
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    cart = request.session.get('cart', {})

    if class_id in list(cart.keys()):
        cart[class_id] += quantity
    else:
        cart[class_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def remove_from_cart(request, class_id):
    """Remove the lesson from the cart."""
    cart = request.session.get('cart', {})

    # Remove the class only if it exists in the cart
    if class_id in cart:
        del cart[class_id]  # Remove the class by its class_id

    request.session['cart'] = cart  # Update the session's cart
    return redirect('view_cart')  # Redirect to the cart view
