import csv
import os
import shutil

import django
from django.core.files.images import ImageFile
import pandas as pd
from config.settings import MEDIA_ROOT, MEDIA_URL

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import feature.models as f
import community.models as c


def insert_posts_category():
    categories = []
    for title in ['질문', '추천', '자유']:
        categories.append(c.Category(
            name    = title
        ))
    c.Category.objects.bulk_create(categories)
    print('DONE: Post Categories')

CSV_PATH = './data/'
def insert_category():
    categories = []
    with open(CSV_PATH+'categories.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if not f.Category.objects.filter(name=row['category']).exists():
                categories.append(f.Category(
                    name    = row['category']
                ))
    f.Category.objects.bulk_create(categories)
    print('DONE: Insert Category data.')

IMAGE_PATH = './data/images/'
MEDIA_FOOD = os.path.join(MEDIA_ROOT, 'images')

def delete_food_images():
    try:
        shutil.rmtree(MEDIA_FOOD)
        print('DELETED: ./media/images/food')
    except OSError as e:
        print("Error: %s : %s" % (MEDIA_FOOD, e.strerror))

def insert_food():
    delete_food_images()
    foods = []
    with open(CSV_PATH+'foods.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name            = row['menu']
            kcal            = row['kcal']
            try:
                image       = ImageFile(open(IMAGE_PATH+name+'.png', 'rb'))
            except:
                image       = ''
            category        = f.Category.objects.get(name=row['category'])
            if not f.Food.objects.filter(name=row['menu']).exists():
                foods.append(f.Food(
                    name    = name,
                    kcal    = kcal,
                    image   = image,
                    category= category
                ))
    f.Food.objects.bulk_create(foods)
    print('DONE: Insert Food data.')

insert_posts_category()
insert_category()
insert_food()