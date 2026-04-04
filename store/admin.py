from django.contrib import admin

# Register your models here.
from .models import Category , Customer , Product , Order , Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)




#mix userinfo and profileinfo
class ProfileInline(admin.StackedInline):
    model = Profile




#extend user
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ["username" , "first_name" , "last_name" , "email"]
    inlines = [ProfileInline]


#unregisterd the old way 
admin.site.unregister(User)

#RE-register the new way
admin.site.register(User , UserAdmin)