from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True,null=True)
    calorie_limit=models.IntegerField(null=True)
    
    def __str__(self):
        return str(self.name)

class Category(models.Model):
    options=(
        ('breakfast','breakfast'),
        ('lunch','lunch'),
        ('dinner','dinner'),
        ('snacks','snacks'),
    )
    name=models.CharField(max_length=50,choices=options)
    def __str__(self):
        return self.name

class Fooditem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ManyToManyField(Category)
    carbohydrate = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    fats = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    protein = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    calorie=models.DecimalField(max_digits=5,decimal_places=2,default=0,blank=True)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    
    def __str__(self):
        return str(self.name)

class Exercise(models.Model):
    name = models.CharField(max_length=200)
    time = models.IntegerField(default=0,blank=True)
    calorie = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    user_id = models.IntegerField(default=0,blank=True)
    
    def __str__(self):
        return str(self.name)

class UserFooditem(models.Model):
    customer = models.OneToOneField(Customer,null=True,on_delete=models.CASCADE)
    fooditem = models.ManyToManyField(Fooditem)
    