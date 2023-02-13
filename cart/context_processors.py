from .cart import Cart
from products.models import Inventory
from django.conf import settings

def cart(request):
    cart = Cart(request)
    if request.user.is_authenticated and not request.session[settings.BASKET_SESSION_ID]:
        if request.user.cart_db_set.count():
            for item in request.user.cart_db_set.all():
                product = Inventory.objects.get(id=item.product_id)
                cart.add(product=product, qty=item.qty)
                cart.__len__()
                      
    return {'cart': cart}