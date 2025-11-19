from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('owner', 'Владелец'),
        ('courier', 'Курьер'),
    )
    phone_number = PhoneNumberField()
    user_photo = models.ImageField(upload_to='user_photo', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client')
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True)
    category_image = models.ImageField(upload_to='category_image')

    def __str__(self):
        return self.category_name


class Store(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_stores')
    store_name = models.CharField(max_length=30, unique=True)
    store_image = models.ImageField(upload_to='store_image')
    store_logo = models.ImageField(upload_to='store_logo')
    store_description = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.store_name}'

    def get_avg_rating (self):
        ratings = self.review_store.all()
        if ratings.exists():
            return round(sum([i.rating for i in ratings]) / ratings.count(), 1)
        return 0

    def get_avg_procent(self):
        ratings = self.review_store.all()
        count_person = 0

        if ratings.exists():
            for r in ratings:
                if r.rating > 3:
                    count_person += 1

            return f'{(count_person * 100) / ratings.count()}%'

        return '0%'

    def get_count_person (self):
        return self.review_store.count()




class Contact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_contacts')
    contact_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.contact_name} - {self.store.store_name}'


class Address(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_addresses')
    address_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.store.store_name} - {self.address_name}'


class StoreMenu(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_menus')
    menu_name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return f'{self.menu_name} - {self.store.store_name}'


class Product(models.Model):
    menu = models.ForeignKey(StoreMenu, on_delete=models.CASCADE, related_name='product_stores')
    product_image = models.ImageField(upload_to='product_image')
    product_name = models.CharField(max_length=50)
    product_price = models.PositiveIntegerField()
    product_description = models.TextField()
    product_quantity = models.PositiveSmallIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_name} - {self.product_price}'


class Order(models.Model):
    ORDER_STATUS = (
        ('processing', 'Обрабатывается'),
        ('ready', 'Готово'),
        ('on_the_way', 'В пути'),
        ('delivered', 'Доставлено'),
        ('cancelled', 'Отменено'),
    )

    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_client')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='processing')
    delivery_address = models.TextField()
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_courier')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.client} - {self.get_status_display()}'


class Courier(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='courier_orders')
    COURIER_STATUS = (
        ('busy', 'Занят'),
        ('available', 'Доступен'),
    )
    status = models.CharField(max_length=20, choices=COURIER_STATUS)

    def __str__(self):
        return f'{self.current_orders} - {self.user} - {self.get_status_display()}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True, related_name='review_store')
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True, related_name='review_courier')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.rating}'
