@echo off
python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py flush --no-input
python ./process_data.py
python ./db_init.py
echo from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '', 'qwer1234!@') | python manage.py shell
python ./manage.py runserver