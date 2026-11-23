from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """Ініціалізація кошика покупця"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Зберігаємо пустий кошик у сесії
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Додати гру до кошика або оновити її кількість"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Позначити сесію як «змінену», щоб вона збереглася"""
        self.session.modified = True

    def remove(self, product):
        """Видалити гру з кошика"""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(items_self):
        """Ітерація по елементах кошика та отримання товарів з бази даних"""
        product_ids = items_self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = items_self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(items_self):
        """Підрахунок загальної кількості товарів у кошику"""
        return sum(item['quantity'] for item in items_self.cart.values())

    def get_total_price(self):
        """Підрахунок загальної вартості кошика"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очищення кошика із сесії"""
        del self.session[settings.CART_SESSION_ID]
        self.save()