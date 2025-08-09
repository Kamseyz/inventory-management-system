from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ProductModel,OrdersModel
from .forms import ProductForm, OrderForm
from django.contrib import messages
from django.utils.timezone import now
from django.db.models import F, Sum, ExpressionWrapper, DecimalField

# Create your views here.


                                                    # Admin dashboard and logic
# list products for admin and worker


class AdminView(LoginRequiredMixin,UserPassesTestMixin, ListView):
    template_name = 'dashboard/admin-dashboard.html'
    context_object_name = 'products'
    model = ProductModel
    paginate_by = 10
    
    
    def get_queryset(self):
        return ProductModel.objects.all().order_by('timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        low_stock_products = ProductModel.objects.filter(quantity__lt=5)
        context['low_stock_products'] = low_stock_products
        context['total_products'] = ProductModel.objects.count()
        context['low_stock_count'] = low_stock_products.count()
        context['recent_orders'] = OrdersModel.objects.select_related('product_name', 'ordered_by').order_by('-ordered_at')[:5]
        
        
        
        # Orders made today
        today = now().date()
        context['orders_today'] = OrdersModel.objects.filter(ordered_at__date=today).count()

        # Revenue: quantity * product_name__price for today
        revenue_qs = OrdersModel.objects.filter(ordered_at__date=today).annotate(
            total_price=ExpressionWrapper(
                F('quantity') * F('product_name__price'),
                output_field=DecimalField()
            )
        ).aggregate(total=Sum('total_price'))

        context['revenue'] = revenue_qs['total'] or 0
        return context
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == "admin"

# add products

class AdminAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    template_name = 'dashboard/add-product.html'
    form_class = ProductForm
    success_url = reverse_lazy('admin-dashboard')
    
    def form_valid(self, form):
        messages.success(self.request, 'Product has been added successfully')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid input try again')
        return super().form_invalid(form)
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == "admin"



#edit products

class AdminEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'dashboard/edit-product.html'
    form_class = ProductForm
    model = ProductModel
    success_url = reverse_lazy('admin-dashboard')
    
    def form_valid(self, form):
        form.instance = self.request
        messages.success(self.request, 'Product has been updated successfully')
        return super().form_valid(form)
    
    def get_queryset(self):
        return ProductModel.objects.filter()
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == "admin"


#delete products


class AdminDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'dashboard/delete-product.html'
    model = ProductModel
    success_url = reverse_lazy('admin-dashboard')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Product was deleted successfully') 
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return ProductModel.objects.filter()
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == "admin"



# show orders to admin
class ShowOrdertoAdmin(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'dashboard/show-order.html'
    model = OrdersModel
    context_object_name = 'orders'

    def test_func(self):
        return self.request.user.role == 'admin'
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_orders'] = OrdersModel.objects.select_related('product_name', 'ordered_by').order_by('-ordered_at')[:5]
        return context


# admin product view list
class ProductView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'dashboard/product-list.html'
    model = ProductModel
    context_object_name = 'products'   

    def test_func(self):
        return self.request.user.role == 'admin'
    
    




                                                        #Worker dashboard and logic here
 
   
#show product to worker   
class ShowProductWorker(LoginRequiredMixin, ListView):
    template_name = 'worker/show-product.html'
    model = ProductModel
    context_object_name ='admin_products'
    
    def get_queryset(self):
        return ProductModel.objects.all()
  
    
                               
#create order
class CreateOrder(LoginRequiredMixin, CreateView):
    template_name = 'worker/create-order.html'
    form_class = OrderForm
    success_url = reverse_lazy('admin-dashboard')
    model = OrdersModel
    
    def form_valid(self, form):
        product = form.cleaned_data.get['product']
        order_qty = form.cleaned_data.get['quantity']
        if product.quantity < order_qty:
            messages.error(self.request, f'Not enough stock for {product.name}. Only {product.quantity}left')
            return self.form_invalid(form)
        
        # reduce product quantity
        product.quantity -= order_qty
        product.save()
        
        # show who ordered
        
        form.instance.ordered_by = self.request.user
        messages.success(self.request, 'Order has been placed')
        return super().form_valid(form)
    
        
        
    
    
    
    
#list order (main dashboard)
class ListOrder(LoginRequiredMixin, ListView):
    template_name = 'worker/dashboard.html'
    model = OrdersModel
    paginate_by = 10
    
    def get_queryset(self):
        return OrdersModel.objects.all().order_by('ordered_at')
    
    
    
#edit order
class EditOrder(LoginRequiredMixin, UpdateView):
    template_name = 'worker/edit-order.html'
    model = OrdersModel
    form_class = OrderForm
    
    
    def form_valid(self, form):
        form.instance = self.request.worker
        messages.success(self.request, 'Order has been updated')
        return super().form_valid(form)
    
    def get_queryset(self):
        return OrdersModel.objects.filter(ordered_by=self.request.user)
    
#delete order
class DeleteOrder(LoginRequiredMixin, DeleteView):
    template_name = 'worker/delete-order.html'
    model = OrdersModel
    success_url = reverse_lazy('worker-dashboard')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Order was deleted successfully') 
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        return OrdersModel.objects.filter(ordered_by=self.request.user)