from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete 
from django.dispatch import receiver

class Day(models.Model):
    tracker = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, blank=True)
    total_cal = models.IntegerField(default=0, blank=True)
    total_protein = models.IntegerField(default=0, blank=True)
    total_carbs = models.IntegerField(default=0, blank=True)
    total_fats = models.IntegerField(default=0, blank=True)

    @classmethod
    def increment(cls, instance, **kwargs):
        instance.total_cal += kwargs['calories']
        instance.total_protein += kwargs['protein']
        instance.total_carbs += kwargs['carbs']
        instance.total_fats += kwargs['fats']
        instance.save()

    @classmethod
    def decrement(cls, instance, **kwargs):
        instance.total_cal -= kwargs['calories']
        instance.total_protein -= kwargs['protein']
        instance.total_carbs -= kwargs['carbs']
        instance.total_fats -= kwargs['fats']
        instance.save()

    def __str__(self): 
        return str(self.date)

class Item(models.Model):
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    calories = models.IntegerField()
    protein = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()

    def __str__(self):
        return self.name + f" consumed by {self.day.tracker.username}"

    def get_absolute_url(self):
        return reverse('home-tracker')


# Before deleting Item instance, it updates Day total calories
@receiver(pre_delete, sender=Item)
def delete_item(sender, instance, **kwargs):
    Day.decrement(
        instance.day, 
        calories=instance.calories,
        protein=instance.protein,
        carbs=instance.carbs,
        fats=instance.fats,
        )