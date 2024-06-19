from django.urls import include, path
from .views import signup
from classes import views

urlpatterns = [
    path('', views.HomePage, name='homepage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginPage, name='loginpage'),
    path('addProduct/', views.AddProduct, name='addProductPage'),
    path('product/', views.Products, name='productPage'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('logoutbutton/', views.logoutbutton, name='logoutbutton'),
    path('cart_page/', views.cart, name='cart_page'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('increase_quantity/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/', views.decrease_quantity, name='decrease_quantity'),
    path('delete_quantity/', views.delete_quantity, name='delete_quantity'),
    path('deleteProduct/<int:product_id>/', views.deleteProduct, name='deleteProduct'),
    path('confirmOrder/', views.confirmOrder, name='confirmOrder'),
    path('order_page_user/', views.userOrder, name='userOrder'),
    path('social-auth/', include('social_django.urls', namespace='social')),
]