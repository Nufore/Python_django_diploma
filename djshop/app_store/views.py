from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView
from .models import Product, ProductPictures, Feedback
from .forms import ReviewAddForm


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_store/product_detail_.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pictures'] = ProductPictures.objects.filter(product=self.object)
        context['reviews'] = Feedback.objects.filter(product=self.object)[:2]
        context['rev_count'] = Feedback.objects.filter(product=self.object).count()
        context['rev_form'] = ReviewAddForm
        return context

    def post(self, request, *args, **kwargs):
        rev_form = ReviewAddForm(request.POST)
        if rev_form.is_valid():
            reply = rev_form.save(commit=False)
            reply.user = request.user
            reply.product = self.get_object()
            reply.save()
            return HttpResponseRedirect(f'/store/product/{reply.product.id}')


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
    template_name = 'app_store/product_list.html'
    context_object_name = 'product_list'


def base(request):
    return render(request, 'app_store/base.html')
