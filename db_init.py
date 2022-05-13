import csv
import os

import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from feature.models import (
    Category, Food
)


CSV_PATH = './data/'
def insert_category():
    categories = []
    with open(CSV_PATH+'categories.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not Category.objects.filter(name=row['category']).exists():
                categories.append(Category(
                    name    = row['category']
                ))
    Category.objects.bulk_create(categories)
    print('DONE: Insert Category data.')

def insert_food():
    foods = []
    with open(CSV_PATH+'foods.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category        = Category.objects.get(name=row['category'])
            if not Food.objects.filter(name=row['menu']).exists():
                foods.append(Food(
                    name    = row['menu'],
                    category= category
                ))
    Food.objects.bulk_create(foods)
    print('DONE: Insert Food data.')

insert_category()
insert_food()