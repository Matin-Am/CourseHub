from . import views
from django.urls import path


app_name = 'order'
urlpatterns = [
    path("cart/add/<slug:course_slug>/",views.CartAddView.as_view(),name='cart_add') ,
    path("cart/remove/<slug:course_slug>/",views.CartRemoveView.as_view(),name="cart_remove"),
    path("cart/",views.CartDetailView.as_view(),name="cart")
]