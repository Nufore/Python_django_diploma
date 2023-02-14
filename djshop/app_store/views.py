from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Product, ProductPictures, Feedback
from .forms import ReviewAddForm


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app_store/product_detail_.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pictures'] = ProductPictures.objects.filter(product=self.object)
        context['reviews'] = Feedback.objects.filter(product=self.object)
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


class ProductListView(ListView):
    model = Product
    template_name = 'app_store/product_list.html'
    context_object_name = 'product_list'


def base(request):
    return render(request, 'app_store/base.html')
