from django.contrib import admin
from .models import Create_subs, CreateUser,Members_eliminated

# Register your models here.


admin.site.register(CreateUser)
admin.site.register(Create_subs)
admin.site.register(Members_eliminated)
