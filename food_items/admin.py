from django.contrib import admin
from .models import FoodItem, AddDate, AddDetail, TotalEnergies


@admin.register(FoodItem)
class UserAdmin(admin.ModelAdmin):
 list_display = ('id','Fooditem', 'Protein', 'Carbohydrates','Fat','Calories')


@admin.register(AddDate)
class AddDateAdmin(admin.ModelAdmin):
 list_display = ['date']


@admin.register(AddDetail)
class AddDetailAdmin(admin.ModelAdmin):
 list_display = ['add_item','id']


@admin.register(TotalEnergies)
class TotalEnergiesAdmin(admin.ModelAdmin):
 list_display = ['date', 'total_pro', 'total_carbo', 'total_fat', 'total_cal']