from decimal import Decimal

from django.conf import settings

from products.models import Product
import uuid

class Cart():
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)
       
        if product_id in self.basket:
            self.basket[product_id]['qty'] = int(qty)             
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

  
        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['subtotal_price'] = item['price'] * int(item['qty'])
            item['total_price'] = item['subtotal_price'] + 50
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return len(self.basket)

    def update(self, product, qty):
        """
        Update values in session data
        """
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = int(qty)
        self.save()

    def get_total_price(self):

        subtotal = sum(Decimal(item['price']) * int(item['qty']) for item in self.basket.values())

        if subtotal == 0:
            shipping = Decimal(0.00)
        else:
            shipping = Decimal(50.00)

        total = subtotal + shipping
        return total

    def get_subtotal_price(self):

        subtotal = sum(Decimal(item['price']) * int(item['qty']) for item in self.basket.values())
        return subtotal

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True