from django.contrib import admin
from .models import Inside, CakeForm, Deko, OutsideColours, OutsideContent, CatalogCake, CakeOrder, \
    CakeBatter, CakeShopAssistant, DekoOrder, Tester

admin.site.register(Inside)
admin.site.register(DekoOrder)
admin.site.register(CakeForm)
admin.site.register(Deko)
admin.site.register(OutsideContent)
admin.site.register(OutsideColours)
admin.site.register(CatalogCake)
admin.site.register(CakeOrder)
admin.site.register(CakeBatter)
admin.site.register(CakeShopAssistant)
admin.site.register(Tester)
