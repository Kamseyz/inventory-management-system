from django.urls import path
from .views import (
    AdminView,
    addproduct,
    AdminAddView,
    AdminEditView,
    AdminDeleteView,
    ShowOrdertoAdmin,
    showadminorder,
    ListOrder,
    # ProductView,
)
urlpatterns = [
     # admin dashboard
    path('dashboard/', AdminView.as_view(), name='admin-dashboard'),
    path('add-product/', AdminAddView.as_view(), name='add-product'),
    # ajax add product
    path('add-product-form/', addproduct, name='add-product-partial'),
    path('edit-product/<int:pk>/', AdminEditView.as_view(), name='edit-product'),
    path('delete-product/<int:pk>/', AdminDeleteView.as_view(), name='delete-product'),
    path('orders/', ShowOrdertoAdmin.as_view(), name='orders'),
    # ajax show order url
    path('orders-form/', showadminorder, name='partial-orders'),
    # path('product-list/', ProductView.as_view(), name='product-list'),

    #worker dashboard

    path('worker/dashboard/', ListOrder.as_view(), name='worker-dashboard'),
   
]
