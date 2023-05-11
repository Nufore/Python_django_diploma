from decimal import Decimal
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from .models import ProductCategory, Product, ProductPictures, Feedback, UserCart, CartList, Delivery, Order,\
    OrderList, Payment, PaymentType, PaymentStatus, DeliveryType
from .forms import ReviewAddForm, UpdateQuantityForm, OrderProfileForm, OrderDeliveryForm, OrderPaymentForm
from django.db.models import Sum, F
from cart.cart import Cart
from cart.forms import CartAddProductForm
from app_users.models import Profile
from payment_api.models import PaymentTransactions
from .forms import AuthForm, OrderRegistryForm, AccountForm


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_store/product_detail_.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pictures'] = ProductPictures.objects.filter(product=self.object)
        context['reviews'] = Feedback.objects.filter(product=self.object)[:2]
        context['rev_count'] = Feedback.objects.filter(product=self.object).count()
        context['rev_form'] = ReviewAddForm
        context['form'] = CartAddProductForm()
        return context

    def post(self, request, *args, **kwargs):
        # product_id = request.POST.get('btn')
        # count = request.POST.get('amount')
        # product = Product.objects.get(id=product_id)
        # cart = UserCart.objects.get(user=request.user)
        # cart_list, created = CartList.objects.get_or_create(cart=cart, product=product, count=count)
        # if not created:
        #     cart_list.count += 1
        #     cart_list.save()

        rev_form = ReviewAddForm(request.POST)
        if rev_form.is_valid():
            reply = rev_form.save(commit=False)
            reply.user = request.user
            reply.product = self.get_object()
            reply.save()
            return HttpResponseRedirect(f'/store/product/{reply.product.id}')

        # return redirect(f'/store/product/{product_id}')


class DynamicReviewLoad(View):

    def get(self, request, *args, **kwargs):
        last_review_id = request.GET.get('lastReviewId')
        product = Feedback.objects.get(id=int(last_review_id)).product
        more_reviews = Feedback.objects.filter(pk__gt=int(last_review_id), product=product)[:2]
        if not more_reviews:
            return JsonResponse({'data': False})
        data = []
        for review in more_reviews:
            obj = {
                'id': review.id,
                'avatar': str(review.user.profile.avatar),
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
                'added_at': review.added_at.strftime("%B %d / %Y / %H:%m"),
                'text': review.text,
            }
            print(obj['avatar'])
            data.append(obj)
        data[-1]['last-review'] = True
        return JsonResponse({'data': data})


class ProductListView(ListView):
    model = Product
    template_name = 'app_store/catalog.html'
    context_object_name = 'product_list'
    paginate_by = 4


def base(request):
    # три избранные категории товаров
    categories = ProductCategory.objects.order_by('id')[:3]
    product_categories_parameters = []
    for item in categories:
        product = Product.objects.filter(category=item).order_by('price').first()
        product_categories_parameters.append({"category": item.name,
                                              "price_from": product.price,
                                              "picture": product.picture})

    # каталог топ-товаров (popular product)(hot offers)
    popular_products = sorted(OrderList.objects.values('product').annotate(Sum('count'))[:8],
                              key=lambda x: x['count__sum'],
                              reverse=True)
    products = [Product.objects.get(id=product['product']) for product in popular_products]

    # слайдер с ограниченным тиражом (Limited edition)
    limited_edition_products = Product.objects.filter(limited_edition=True).order_by('id')[:16]

    return render(request, 'app_store/base.html', {'product_categories_parameters': product_categories_parameters,
                                                   'products': products,
                                                   'limited_edition_products': limited_edition_products})


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = UserCart.objects.get(user=request.user)
            cart_list = CartList.objects.select_related('product').filter(cart=cart)
            cart_summ = CartList.objects.filter(cart=cart).aggregate(total=Sum(F('product__price') * F('count')))
            form = UpdateQuantityForm()
            return render(request, 'app_store/cart.html', context={'cart_list': cart_list,
                                                                   'cart_summ': cart_summ['total'],
                                                                   'form': form})
        else:
            cart = Cart(request)
            form = UpdateQuantityForm()
            return render(request, 'app_store/cart.html', {'cart': cart,
                                                           'form': form})

    def post(self, request):
        if request.POST.get('btn_add'):
            product_id = request.POST.get('btn_add')
            update_cnt = 1
            product = Product.objects.get(id=product_id)
            cart = Cart(request)
            cart.add(product=product, quantity=update_cnt, update_quantity=False)
        elif request.POST.get('btn_remove'):
            product_id = request.POST.get('btn_remove')
            update_cnt = -1
            product = Product.objects.get(id=product_id)
            cart = Cart(request)
            cart.add(product=product, quantity=update_cnt, update_quantity=False)

        return redirect('/store/cart/')


def product_list(request):
    category = None
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    return render(request, 'app_store/product/list.html', context={'category': category,
                                                                   'categories': categories,
                                                                   'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    cart_product_form = CartAddProductForm()
    return render(request, 'app_store/product/detail.html', {'product': product,
                                                             'cart_product_form': cart_product_form})


class OrderDeliveryView(View):
    base_delivery = DeliveryType.objects.get(is_express=False)
    express_delivery = DeliveryType.objects.get(is_express=True)

    def get(self, request):
        if request.user.is_authenticated:
            order_profile_form = OrderProfileForm(instance=Profile.objects.get(user=request.user))
            cart = UserCart.objects.get(user=request.user)
            cart_list = CartList.objects.select_related('product').filter(cart=cart)
        else:
            order_profile_form = OrderProfileForm()
            cart_list = Cart(request)
        order_registry_form = OrderRegistryForm()
        login_form = AuthForm()
        order_delivery_form = OrderDeliveryForm()
        order_payment_form = OrderPaymentForm()

        context = {'order_profile_form': order_profile_form,
                   'order_registry_form': order_registry_form,
                   'order_delivery_form': order_delivery_form,
                   'order_payment_form': order_payment_form,
                   'login_form': login_form,
                   'cart_list': cart_list,
                   'base_delivery': self.base_delivery,
                   'express_delivery': self.express_delivery}

        return render(request, 'app_store/order.html', context=context)

    def post(self, request):

        if request.POST.get('btn_login'):
            login_form = AuthForm(request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect('/store/order')
                    else:
                        login_form.add_error('__all__', 'Ошибка! Учетная запись пользователя не активна.')
                else:
                    login_form.add_error('__all__', 'Ошибка! Проверьте правильность ввода логина и пароля.')
            return render(request, 'app_store/order.html', {'login_form': login_form,
                                                            'order_registry_form': OrderRegistryForm(),
                                                            'base_delivery': self.base_delivery,
                                                            'express_delivery': self.express_delivery})

        if request.POST.get('btn_register'):
            order_registry_form = OrderRegistryForm(request.POST)
            login_form = AuthForm(request.POST)
            if order_registry_form.is_valid():
                fio = order_registry_form.cleaned_data.get('fio')
                phone_number = order_registry_form.cleaned_data.get('phone_number')
                email = order_registry_form.cleaned_data.get('email')
                password1 = order_registry_form.cleaned_data.get('password1')
                password2 = order_registry_form.cleaned_data.get('password2')

                if User.objects.filter(email=email).exists():
                    login_form.add_error('__all__', 'Пользователь с указанным email существует, вы можете авторизоваться')
                    return render(request, 'app_store/order.html', {'login_form': login_form,
                                                                    'order_registry_form': order_registry_form,
                                                                    'base_delivery': self.base_delivery,
                                                                    'express_delivery': self.express_delivery})

                if password1 != password2:
                    order_registry_form.add_error('__all__', ['Ошибка!', 'Введенные пароли не совпадают!'])
                else:
                    anon_cart = Cart(request)
                    user = User.objects.create_user(username=email, email=email, password=password1)
                    cart = UserCart.objects.create(user=user)
                    for item in anon_cart:
                        CartList.objects.create(cart=cart,
                                                product=Product.objects.get(id=int(item['product'].id)),
                                                count=int(item['quantity']))
                    Profile.objects.create(
                        user=user,
                        fio=fio,
                        phone_number=phone_number
                    )
                    anon_cart.clear()
                    user = authenticate(username=email, password=password1)
                    login(request, user)
                    return redirect('/store/order')
                return render(request, 'app_store/order.html', {'order_registry_form': order_registry_form,
                                                                'login_form': login_form,
                                                                'base_delivery': self.base_delivery,
                                                                'express_delivery': self.express_delivery})

        order_delivery_form = OrderDeliveryForm(data=request.POST)
        if order_delivery_form.is_valid():
            city = order_delivery_form.cleaned_data.get('city')
            address = order_delivery_form.cleaned_data.get('address')
            del_type = order_delivery_form.cleaned_data.get('delivery_type')
            if del_type == 'Экспресс доставка KEY':
                delivery_type = DeliveryType.objects.get(is_express=True)
            elif del_type == 'Обычная доставка KEY':
                delivery_type = DeliveryType.objects.get(is_express=False)
            delivery = Delivery.objects.create(type=delivery_type, city=city, address=address)

        order_payment_form = OrderPaymentForm(data=request.POST)
        if order_payment_form.is_valid():
            pay_type = order_payment_form.cleaned_data.get('payment_type')
            if pay_type == 'Онлайн картой KEY':
                payment = Payment.objects.create(type=PaymentType.objects.get(id=1),
                                                 status=PaymentStatus.objects.get(id=2))
            elif pay_type == 'Онлайн со случайного чужого счета KEY':
                payment = Payment.objects.create(type=PaymentType.objects.get(id=2),
                                                 status=PaymentStatus.objects.get(id=2))

        cart = UserCart.objects.get(user=request.user)
        cart_list = CartList.objects.select_related('product').filter(cart=cart)
        cart_summ = CartList.objects.filter(cart=cart).aggregate(total=Sum(F('product__price') * F('count')))

        if delivery_type.is_express:
            total_cost = float(cart_summ['total']) + delivery_type.express_price
        else:
            if float(cart_summ['total']) >= delivery_type.base_less_than:
                total_cost = float(cart_summ['total'])
            else:
                total_cost = float(cart_summ['total']) + delivery_type.base_price

        new_order = Order.objects.create(user=request.user, total_cost=total_cost, delivery=delivery,
                                         payment=payment)
        for item in cart_list:
            OrderList.objects.create(order=new_order, product=item.product, count=item.count)

        cart.delete()

        return redirect(f'/store/order-detail/{new_order.id}')


class OrderDetailView(DetailView):
    model = Order
    template_name = 'app_store/oneorder.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_list'] = OrderList.objects.filter(order=self.object)
        return context


class PaymentView(View):
    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        account_form = AccountForm()
        return render(request, 'app_store/payment.html', {'order': order,
                                                          'account_form': account_form})

    def post(self, request, pk):
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            order = Order.objects.get(id=pk)
            account = int(account_form.cleaned_data.get('account').replace(' ', ''))
            payment, created = PaymentTransactions.objects.get_or_create(order_id=pk)
            payment.account = account
            if created:
                payment.summ = order.total_cost
            payment.save()
            return redirect(f'/store/progress-payment/{pk}')


def progress_payment(request, pk):
    return render(request, 'app_store/progressPayment.html', {'pk': pk})


class OrderListView(ListView):
    model = Order
    template_name = 'app_store/historyorder.html'
    context_object_name = 'order_list'
    ordering = '-id'


class HistoryOrderView(View):

    def get(self, request):
        order_list = Order.objects.filter(user=request.user).order_by('-id')
        return render(request, 'app_store/historyorder.html', {'order_list': order_list})


class GetPaymentResponse(View):

    def get(self, request, pk):
        order = Order.objects.get(id=pk)
        if order.payment.status.id == 1:
            return JsonResponse({'data': True})
        else:
            return JsonResponse({'data': False})
