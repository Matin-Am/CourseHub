from .cart import Cart



def cart(request):
    return {"cart":Cart(request,request.user.username)}