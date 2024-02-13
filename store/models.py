from django.db import models
from Face_Recog.models import *
import datetime


# Category Model 
class Category(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


    def __str__(self):
        return self.name

# Product Category
class Product(models.Model):
    idProduct = models.IntegerField(primary_key=True, default='')
    name = models.CharField(max_length =50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to = 'products/')
    

    @staticmethod
    def getProductsById(ids):
        return Product.objects.filter(idProduct__in =ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()

    def __str__(self):
        return self.name


# Order model
class Order(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    customer = models.ForeignKey(UserProfile,
                                 on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField()
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    