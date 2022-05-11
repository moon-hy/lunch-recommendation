# init

0. pip install django djangorestframework django-cors-headers drf-yasg flex Pillow
1. python manage.py makemigrations
2. python manage.py migrate
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

- 사용자의 선호 음식, 비선호 음식 검색
- 추천 결과 반환 API
- ...
