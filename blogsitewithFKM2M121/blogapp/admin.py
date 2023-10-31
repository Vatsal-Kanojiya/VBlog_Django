from django.contrib import admin
from .models import blog,comment,bloguser,smarttransaction
# Register your models here.

# class BlogusersimpleAdmin(admin.ModelAdmin):
#     prepopulated_fields={'slug':('username',)} 
#     #list_filter=('day','month','year','status','task')
#     list_display=('id','idu','username','status')
#     list_display_links=('username',)
# admin.site.register(blogusersimple,BlogusersimpleAdmin)

class BloguserAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('email',)} 
    #list_filter=('day','month','year','status','task')
    list_display=('id','idu','email','status')
    list_display_links=('email',)
admin.site.register(bloguser,BloguserAdmin)

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)} 
    #list_filter=('day','month','year','status','task')
    list_display=('id','idb','title','genre')
    list_display_links=('title',)
admin.site.register(blog,BlogAdmin)


class CommentAdmin(admin.ModelAdmin):
    #prepopulated_fields={'slug':('idc',)} 
    #list_filter=('day','month','year','status','task')
    list_display=('id','idc','idb','idu','date_of_comment')
    list_display_links=('idc',)
admin.site.register(comment,CommentAdmin)



class SmarttransactionAdmin(admin.ModelAdmin):
    # prepopulated_fields={'slug':('idc','idu')} 
    #list_filter=('day','month','year','status','task')
    list_display=('id','idc','idu','razor_pay_order_id','payment_status','transaction_dt_tm')
    list_display_links=('razor_pay_order_id',)
admin.site.register(smarttransaction,SmarttransactionAdmin)

