# init


0. pip install django djangorestframework django-cors-headers drf-yasg flex Pillow mysqlclient scikit-learn pandas numpy
0. (OR) pip install -r requirements.txt
1. ./init_for_test.bat (아래의 과정을 포함)
    1. python manage.py makemigrations
    2. python manage.py migrate
        > DB 초기화: python manage.py flush
    0. python process_data.py
    0. python db_init.py
    3. python manage.py createsuperuser
    4. python manage.py runserver

+ Header
    - Authorization: Token {Token}

# API Docs

- /redoc (ex. localhost:8000/redoc)

# secrets.json

>{  
>"SECRET_KEY": "{MY SECRET KEY}",  
>"DEBUG": "True"  
>}

# runserver

1. python manage.py runserver

# todo

- 추천 결과 반환 API
- ...
