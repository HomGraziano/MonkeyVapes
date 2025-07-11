from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('item/add/', views.item_create, name='item_create'),
    path('order/add/', views.order_create, name='order_create'),
    path('', views.item_list, name='item_list'),
    path('item/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('item/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('order/<int:pk>/delete/', views.order_delete, name='order_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)