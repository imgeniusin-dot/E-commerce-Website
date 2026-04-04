from .cart import Cart

#create context_processors so our cart work on all pages 
def cart(request):
    #return the default data from our cart 
    return { 'cart':Cart(request)}