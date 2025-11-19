from .models import Category, Store, Contact, Address, StoreMenu, Product
from modeltranslation.translator import TranslationOptions,register

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name',)

@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'store_description')

@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('contact_name',)

@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('address_name',)

@register(StoreMenu)
class StoreMenuTranslationOptions(TranslationOptions):
    fields = ('menu_name',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'product_description')