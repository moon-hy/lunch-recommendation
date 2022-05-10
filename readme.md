# init

0. pip install django djangorestframework django-cors-headers Pillow
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py createsuperuser
4. login required


# end points

1. Registration
    - POST /api/user
        - username
        - password
        - password2
        - nickname
        - email

2. Get Token
    - POST /api/auth/token
        - username
        - password

3. Header
    - "Authorization": "Token {Token}"

---

- /api/user
    - GET: Get user list
    - POST: Register

- /api/user/{int:pk}
    - GET: Get user profile
    - PUT: Update user profile
    - PATCH: Update user profile (partial) 
    - DELETE: Deactivate user

---

- /api/auth/token
    - POST: Get token

---

- /api/food
    - GET: Get food list
    - POST: Add food

- /api/food/{int:pk}
    - GET: Get food information
    - PUT: Update food information
    - PATCH: Update food information (partial)
    - DELETE: Delete food

- /api/food/{int:pk}/reviews
    - GET: Get food's reviews
    - POST: Add food's reviews

- /api/food/reviews/{int:pk}
    - GET: Get review detail
    - DELETE: Delete review

- /api/food/categories
    - GET: Get category list
    - POST: Add category

- /api/food/categories/{int:pk}
    - GET: Get specific category's information (ex. related food)

---

- /api/post
    - GET: Get post list
        - Params
            - q: search title (not required)
            - u: search username (not required)
            - s: sort by (not required)
                - comment
    - POST: Add post

- /api/post/{int:pk}
    - GET: Get post detail
    - PUT: Update post
    - PATCH: Update post (partial)
    - DELETE: Delete post

- /api/post/{int:pk}/comments
    - GET: Get post's comments
    - POST: Add post's comment

- /api/post/comments/{int:pk}
    - GET: Get comment's detail
    - DELETE: Delete comment


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
