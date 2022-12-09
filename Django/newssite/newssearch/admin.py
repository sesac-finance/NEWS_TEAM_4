from django.contrib import admin
from .models import TbUser, TbDomain, TbNews, TbComment

# Register your models here.
admin.site.register(TbUser)
admin.site.register(TbNews)
admin.site.register(TbDomain)
admin.site.register(TbComment)