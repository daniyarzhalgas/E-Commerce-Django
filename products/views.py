from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.http import HttpResponseRedirect
from .models import Product
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        product = self.get_object()

        # Track last watched products
        last_watched = request.session.get("last_watched", [])

        if not isinstance(last_watched, list):
            last_watched = []

        if product.pk in last_watched:
            last_watched.remove(product.pk)

        last_watched.insert(0, product.pk)
        last_watched = last_watched[:5]

        request.session["last_watched"] = last_watched
        request.session.modified = True

        return super().get(request, *args, **kwargs)


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    permission_required = "products.add_product"
    success_url = reverse_lazy('product_list')


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'products/product_form.html'
    form_class = ProductForm
    permission_required = "products.change_product"
    success_url = reverse_lazy('product_list')


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    permission_required = "products.delete_product"
    success_url = reverse_lazy('product_list')


class UserLoginView(LoginView):
    template_name = "auth/login.html"


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        last_watched_ids = request.session.get("last_watched", [])
        products = list(Product.objects.filter(id__in=last_watched_ids))
        products.sort(key=lambda p: last_watched_ids.index(p.id))
        return render(request, "auth/profile.html", {"viewed_products": products})
