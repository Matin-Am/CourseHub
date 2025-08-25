from . import views
from django.urls import path


app_name = 'order'
urlpatterns = [
    path("cart/add/<slug:course_slug>/",views.CartAddView.as_view(),name='cart_add') ,
    path("cart/remove/<slug:course_slug>/",views.CartRemoveView.as_view(),name="cart_remove"),
    path("cart/",views.CartDetailView.as_view(),name="cart"),
    path("create/",views.OrderCreateView.as_view(),name="order_create"),
    path("pay/<int:order_id>/",views.OrderPayView.as_view(),name="order_pay"),
    path("detail/<int:order_id>/",views.OrderDetailView.as_view(),name="detail"),
    path("coupon/<int:order_id>/",views.CouponApplyView.as_view(),name='coupon')
]