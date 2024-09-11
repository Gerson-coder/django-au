from django.contrib import admin
from .models import Create_subs, Create_members,Members_eliminated

# Register your models here.


admin.site.register(Create_members)
admin.site.register(Create_subs)
admin.site.register(Members_eliminated)
