import csv
import os
import shutil
import random
from datetime import timedelta

import django
from django.utils import timezone
from django.core.files.images import ImageFile
from django.contrib.auth import get_user_model
import pandas as pd
from config.settings import MEDIA_ROOT

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

User    = get_user_model()
def update_admin():
    user        = User.objects.get(username='admin')
    profile     = user.profile
    profile.nickname = 'admin'
    profile.interest_in = f.Category.objects.get(pk=1)
    profile.save()

    user    = User.objects.get(username='admin')
    interest= user.profile.interest_in

    all_cats= f.Category.objects.all()
    weights     = [1]*len(all_cats)
    weights[interest.id-1]= 3
    candidates = random.choices(all_cats, weights, k=20)

    now         = timezone.now()
    for day, category in enumerate(candidates):
        food    = random.choice(category.foods.all())
        history = f.History.objects.create(
            food=food,
            user=user,
        )
        history.created_at = now-timedelta(days=day+1)
        history.save(update_fields=['created_at'])

    print('DONE: Update admin. Set admin\'s interest_in = {Category_id:1}')

user_size= 30
def create_users():
    for i in range(1,user_size+1):
        user    = User(
            username    = f'test{i}',
            password    = 'qwer1234!@',
        )
        user.save()
        profile = user.profile
        profile.nickname = f'test{i}'
        profile.interest_in = f.Category.objects.get(pk=((i-1)%8+1))
        profile.save()
    print(f'DONE: Create users: <test1 ~ test{user_size}>')

history_size = 20
def create_histories():
    now         = timezone.now()

    for i in range(1,user_size+1):
        user    = User.objects.get(username=f'test{i}')
        interest= user.profile.interest_in

        all_cats= f.Category.objects.all()
        weights     = [1]*len(all_cats)
        weights[interest.id-1]= 3
        candidates = random.choices(all_cats, weights, k=history_size)

        for day, category in enumerate(candidates):
            food    = random.choice(category.foods.all())
            history = f.History.objects.create(
                food=food,
                user=user,
            )
            history.created_at = now-timedelta(days=day+1)
            history.save(update_fields=['created_at'])

    print(f'DONE: Create histories by considering their interest ({hitsory_size} histories per person')

def createCSV():
    histories   = f.History.objects.all()[:]
    df          = pd.DataFrame()

    for history in histories:
        tmp     = pd.DataFrame(
            {
                'user': [history.user.id],
                'food': [history.food.id],
                'date(utc)': [history.created_at]
            }
        )
        df      = pd.concat([df, tmp])
    df.to_csv(f'./data/history_test.csv', index=False)
    print('DONE: Create CSV file of history to \'./data/history_test.csv\'. (For ML or DS, \'date\': UTC)')

    foods       = f.Food.objects.all()[:]
    df          = pd.DataFrame()
    for food in foods:
        tmp     = pd.DataFrame(
            {
                'food_name': [food.name],
                'food_category': [food.category.name],
                'food_id': [food.id]
            }
        )
        df      = pd.concat([df, tmp])
    df.to_csv(f'./data/food_test.csv', index=False)

    print('DONE: Create CSV file of history to \'./data/food_test.csv\'. (For ML or DS)')

insert_posts_category()
insert_category()
insert_food()
update_admin()
create_users()
create_histories()
createCSV()
