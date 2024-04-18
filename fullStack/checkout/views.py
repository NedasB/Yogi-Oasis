from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.db import transaction
import stripe

from .forms import OrderForm
from .models import Order, OrderLineItem
from classes.models import Lesson as Class
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from cart.contexts import cart_contents

def checkout(request):
    # Handle POST request for checkout
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('cart', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.save()

            try:
                with transaction.atomic():
                    for class_id, quantity in bag.items():
                        class_obj = Class.objects.get(id=class_id)
                        # Check if there's enough space in the class
                        if class_obj.current_capacity + quantity > class_obj.max_capacity:
                            messages.error(request, (
                                "There's not enough space in one of the classes. "
                                "Please adjust your cart or contact us for assistance."
                            ))
                            return redirect('view_cart')

                        class_obj.current_capacity += quantity
                        class_obj.save()

                        OrderLineItem.objects.create(
                            order=order,
                            lesson=class_obj,
                            quantity=quantity
                        )
                # Save the info to the user's profile if all is well
                request.session['save_info'] = 'save-info' in request.POST
                return redirect(reverse('checkout_success', args=[order.order_number]))
               
            # If the class is not found, delete the order and return an error
            except Class.DoesNotExist:
                messages.error(request, (
                    "One of the classes in your cart wasn't found in our database. "
                    "Please call us for assistance!"
                ))
                order.delete()
                return redirect(reverse('view_bag'))
        # If the form is invalid, return an error
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect(reverse('classes'))
        
        current_cart = cart_contents(request)
        total = current_cart['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        # Attempt to prefill the form with any info the user maintains in their profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)


# Handle successful checkouts
def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    # Attach the user's profile to the order
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']
    
    context = {
        'order': order,
    }

    return render(request, 'checkout/checkout_success.html', context)
