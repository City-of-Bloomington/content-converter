from django.contrib import admin

# Register your models here.
from .models import Page, Conversion, DepartmentPage, PageTopic

admin.site.register(Page)
admin.site.register(Conversion)
admin.site.register(DepartmentPage)
admin.site.register(PageTopic)
