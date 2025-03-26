from django.contrib import admin
from .models import post,aboutus,img,offer,CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class AdminUser(UserAdmin):
    list_display = ['username','email','first_name','last_name']

admin.site.register(CustomUser,AdminUser)

class postAdmin(admin.ModelAdmin):
    
    search_fields= ('title','content')
    list_filter =  ('create_at',)
admin.site.register(post,postAdmin)
admin.site.register(aboutus)
admin.site.register(img)
admin.site.register(offer)
