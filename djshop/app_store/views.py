from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView
from .models import ProductCategory, Product, ProductPictures, Feedback, UserCart, CartList
from .forms import ReviewAddForm, UpdateQuantityForm
from django.db.models import Sum, F
from cart.cart import Cart
from cart.forms import CartAddProductForm


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
    paginate_by = 2


def base(request):
    return render(request, 'app_store/base.html')


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
            return render(request, 'app_store/cart.html', {'cart': cart})

    def post(self, request):
        if request.POST.get('btn_add'):
            product_id = request.POST.get('btn_add')
            update_cnt = 1
        elif request.POST.get('btn_remove'):
            product_id = request.POST.get('btn_remove')
            update_cnt = -1
        product = Product.objects.get(id=product_id)
        cart = UserCart.objects.get(user=request.user)
        cart_list = CartList.objects.get(cart=cart, product=product)
        cart_list.count += update_cnt
        cart_list.save()
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
