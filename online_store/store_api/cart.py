from decimal import Decimal
from django.conf import settings
from django.db.models import Sum, F
from store_api.models import Product, UserCart, CartList


class Cart(object):

    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        if request.user.is_authenticated:
            self.cart, created = UserCart.objects.get_or_create(user=request.user)
        else:
            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
                # save an empty cart in the session
                cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        if isinstance(self.cart, UserCart):
            cart_list, created = CartList.objects.get_or_create(cart=self.cart, product=product)
            if update_quantity:
                cart_list.count = quantity
                cart_list.save()
            else:
                if cart_list.count + quantity > 0:
                    cart_list.count += quantity
                    cart_list.save()
                else:
                    cart_list.delete()
        else:
            product_id = str(product.id)
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0,
                                         'price': str(product.price)}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
            self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, product):
        """
        Удаление товара из корзины.
        """
        if isinstance(self.cart, UserCart):
            cart_list = CartList.objects.get(cart=self.cart, product=product)
            cart_list.delete()
        else:
            product_id = str(product.id)
            if product_id in self.cart:
                del self.cart[product_id]
                self.save()

    def __iter__(self):
        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        if isinstance(self.cart, UserCart):
            pass
        else:
            product_ids = self.cart.keys()
            # получение объектов product и добавление их в корзину
            products = Product.objects.filter(id__in=product_ids)
            for product in products:
                self.cart[str(product.id)]['product'] = product

            for item in self.cart.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        if isinstance(self.cart, UserCart):
            quantity = CartList.objects.filter(cart=self.cart).aggregate(total=Sum(F('count')))
            return quantity['total']
        else:
            return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        if isinstance(self.cart, UserCart):
            cart_summ = CartList.objects.filter(cart=self.cart).aggregate(total=Sum(F('product__price') * F('count')))
            return Decimal(cart_summ['total'])
        else:
            return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True