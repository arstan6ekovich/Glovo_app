from django.contrib import admin
from .models import UserProfile, Category, Store, Contact, Address, StoreMenu, Product, Order, Courier, Review
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin


class AddressInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Address
    extra = 1

class ContactInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = Contact
    extra = 1

class StoreMenuInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = StoreMenu
    extra = 1


@admin.register(Category, Product)
class ProductAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Store)
class ProductAdmin(TranslationAdmin):
    inlines = [AddressInline, ContactInline, StoreMenuInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(Review)