# init

1. python manage.py makemigrations post, food
2. python manage.py migrate
3. python manage.py createsuperuser
4. login required


# end points

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
><br><br><br><br>"SECRET_KEY": "{MY SECRET KEY}",  
><br><br><br><br>"DEBUG": "True"  
>}

# runserver

1. python manage.py runserver
