from django.contrib import admin

from delivery.models import Delivery, DeliveryUser

admin.site.register(Delivery)
admin.site.register(DeliveryUser)
