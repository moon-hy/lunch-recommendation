# init

0. pip install django djangorestframework django-cors-headers Pillow
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py createsuperuser
4. login required


# end points

- /api/user
    - GET
    - POST

- /api/user/{int:pk}
    - GET
    - PUT
    - PATCH
    - DELETE

---

- /api/auth/token
    - POST

---

- /api/food
    - GET
    - POST

- /api/food/{int:pk}
    - GET
    - PUT
    - PATCH
    - DELETE

- /api/food/{int:pk}/reviews
    - GET
    - POST

- /api/food/reviews{int:pk}
    - GET
    - DELETE

---

- /api/post
    - GET
    - POST
    - Params
        - q: search title (not required)
        - u: search username (not required)
        - s: sort by (not required)
            - comment

- /api/post/{int:pk}
    - GET
    - PUT
    - PATCH
    - DELETE

- /api/post/{int:pk}/comments
    - GET
    - POST

- /api/post/comments/{int:pk}
    - GET
    - DELETE


# secrets.json

>{  
>"SECRET_KEY": "{MY SECRET KEY}",  
>"DEBUG": "True"  
>}

# runserver

1. python manage.py runserver

# todo

- 사용자의 선호 음식, 비선호 음식 검색
- 사용자가 결정한 음식 데이터 저장
- 추천 결과 반환 API
- ...