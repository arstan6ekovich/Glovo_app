from rest_framework import serializers
from .models import UserProfile, Category, Store, Contact, Address, StoreMenu, Product, Order, Courier, Review
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'username', 'email', 'password',
                  'phone_number', 'role', 'user_photo')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'email': instance.email,
                'phone_number': instance.phone_number
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'first_name': instance.first_name,
                'last_name': instance.last_name,
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'first_name', 'last_name', 'user_photo')


class UserProfileOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'phone_number')


class UserProfileDetailSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(format('%d-%m-%Y %H-%m'))
    date_joined = serializers.DateTimeField(format('%d-%m-%Y %H-%m'))
    date_registered = serializers.DateTimeField(format('%d-%m-%Y %H-%m'))

    class Meta:
        model = UserProfile
        fields = ('id', 'last_login', 'is_superuser', 'username',
                  'first_name', 'last_name', 'email', 'is_staff',
                  'is_active', 'date_joined', 'phone_number', 'user_photo',
                  'role', 'date_registered', 'groups', 'user_permissions')


class CategoryListSerializer (serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'category_image')


class StoreListSerializer (serializers.ModelSerializer):
    created_date = serializers.DateField(format('%d-%m-%Y'))
    get_avg_rating = serializers.SerializerMethodField()
    get_count_person = serializers.SerializerMethodField()
    get_avg_procent = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ('id', 'store_name', 'store_image', 'store_logo',
                  'created_date', 'get_avg_rating', 'get_count_person', 'get_avg_procent')

    def get_avg_rating(self, object):
        return self.get_avg_rating.object()

    def get_count_person(self, object):
        return self.get_count_person.object()

    def get_avg_procent(self, object):
        return self.get_avg_procent.object()


class ContactSerializer (serializers.ModelSerializer):
    store = StoreListSerializer()

    class Meta:
        model = Contact
        fields = ('contact_name', 'phone_number', 'email', 'store')


class AddressSerializer (serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('address_name',)


class ProductListSerializer (serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Product
        fields = ('id', 'product_image', 'product_name',
                  'product_price', 'product_description', 'product_quantity', 'created_date')


class ProductStoreMenuSerializer (serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')

    class Meta:
        model = Product
        fields = ('product_image', 'product_name',
                  'product_price', 'product_description', 'product_quantity', 'created_date')


class StoreMenuListSerializer (serializers.ModelSerializer):
    product_stores = ProductStoreMenuSerializer(many=True, read_only=True)

    class Meta:
        model = StoreMenu
        fields = ('id', 'menu_name', 'product_stores')


class StoreMenuName (serializers.ModelSerializer):
    class Meta:
        model = StoreMenu
        fields = ('menu_name',)


class ProductDetailSerializer (serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    menu = StoreMenuName()

    class Meta:
        model = Product
        fields = ('id', 'created_date', 'product_image', 'product_name',
                  'product_price', 'product_description', 'product_quantity', 'menu')



class StoreMenuDetailSerializer (serializers.ModelSerializer):
    product_stores = ProductStoreMenuSerializer(many=True, read_only=True)

    class Meta:
        model = StoreMenu
        fields = ('menu_name', 'product_stores')


class OrderSerializer (serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    client = UserProfileOrderSerializer()
    courier = UserProfileOrderSerializer()
    product = ProductListSerializer()

    class Meta:
        model = Order
        fields = ('id', 'client', 'product', 'status', 'delivery_address', 'courier', 'created_at')


class CourierSerializer (serializers.ModelSerializer):
    user = UserProfileOrderSerializer()
    current_orders = OrderSerializer()

    class Meta:
        model = Courier
        fields = ('id', 'user', 'current_orders', 'status')


class ReviewDetailSerializer (serializers.ModelSerializer):
    user = UserProfileOrderSerializer()
    store = StoreListSerializer()

    class Meta:
        model = Review
        fields = ('rating', 'comment', 'user', 'store')


class ReviewSerializer (serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class StoreDetailSerializer (serializers.ModelSerializer):
    created_date = serializers.DateField(format('%d-%m-%Y'))
    user = UserProfileListSerializer()
    category = CategoryListSerializer()
    store_contacts = ContactSerializer(many=True, read_only=True)
    store_addresses = AddressSerializer(many=True, read_only=True)
    store_menus = StoreMenuListSerializer(many=True, read_only=True)


    class Meta:
        model = Store
        fields = ('id', 'store_name', 'store_image', 'store_logo',
                  'store_description', 'created_date', 'user', 'category',
                  'store_contacts', 'store_addresses', 'store_menus')


class CategoryDetailSerializer (serializers.ModelSerializer):
    category_stores = StoreListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'category_name', 'category_image', 'category_stores')









