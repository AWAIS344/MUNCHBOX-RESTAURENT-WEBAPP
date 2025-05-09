from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Comment)
admin.site.register(models.Restaurant)
admin.site.register(models.BlogPost)
admin.site.register(models.Review)
admin.site.register(models.OrderItem)
admin.site.register(models.Order)
admin.site.register(models.PaymentMethod)
admin.site.register(models.Address)
admin.site.register(models.MenuItem)
admin.site.register(models.Package)
admin.site.register(models.Cuisine)
admin.site.register(models.Profile)


