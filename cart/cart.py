
from store.models import Product , Profile

class Cart():
    def __init__(self , request):
        self.session = request.session

        self.request = request

        #get the current session key if it exits 

        cart = self.session.get('session_key')

        #if the user is new no session key so lets create it 

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # make cart available for all pages
        self.cart = cart



    def db_add(self , product , quantity):
        product_id = str(product)
        product_qty = str(quantity)
        #logic 
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True


        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'" , "\"")  

            current_user.update(old_cart=str(carty))




    def add(self , product , quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        #logic 
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True


        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'" , "\"")  

            current_user.update(old_cart=str(carty))


    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart

        totals = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    price = product.sale_price if product.sale else product.price
                    totals = totals + price * value
        return totals
    
    

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #get ids from carts
        product_ids = self.cart.keys()

        #use ids to lookup products in database
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    def update(self , product , quantity):
        product_id = str(product)
        product_qty = int(quantity)
        # get the cart 
        ourcart = self.cart
        # update dictionery/cart
        ourcart[product_id] = product_qty
        self.session.modified = True

        

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'" , "\"")  

            current_user.update(old_cart=str(carty))



        thing = self.cart 
        return thing
    
    def delete(self , product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True


        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'" , "\"")  

            current_user.update(old_cart=str(carty))