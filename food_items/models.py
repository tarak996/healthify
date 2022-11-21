from django.db import models
from django.contrib.auth.models import User



class FoodItem(models.Model):
    Fooditem = models.CharField(max_length=70, null=True)
    Protein = models.IntegerField()
    Carbohydrates = models.IntegerField(null=True)
    Fat = models.IntegerField(null=True)
    Calories = models.IntegerField(null=True)

    def __str__(self):
        return self.Fooditem


class AddDate(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
     date = models.DateTimeField(null=True, unique=True)

     def __str__(self):
         return str(self.date)


class AddDetail(models.Model):
    add_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    date_d = models.ForeignKey(AddDate, on_delete=models.CASCADE, null=True, default=AddDate, editable=False)


class TotalEnergies(models.Model):
    date = models.ForeignKey(AddDate, on_delete=models.CASCADE)
    total_pro = models.IntegerField()
    total_carbo = models.IntegerField()
    total_fat = models.IntegerField()
    total_cal = models.IntegerField()



